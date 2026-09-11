"""Run with: python3 -m unittest discover -s benchmarks/cross-language -v"""

import contextlib
import io
import json
import math
from pathlib import Path
import random
import runpy
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace

import run


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.runtime = run.Runtime("test", Path(sys.executable), Path("source.py"), internal_scale=0.001)

    def test_checksum_and_scale(self):
        self.assertEqual(run.parse_internal_time(self.runtime, "arithmetic", "banner\n10000000\n1e3\n"), 1)

    def test_reject_invalid_outputs(self):
        for output in ("10000000\n", "9999999\n12\n", "12\n10000000\n",
                       "10000000\n12\n42\n", "10000000\n-1\n", "10000000\nnan\n",
                       "10000000\n1e999\n", "1e7\n12\n"):
            with self.subTest(output=output), self.assertRaises(ValueError):
                run.parse_internal_time(self.runtime, "arithmetic", output)

    def test_optional_and_explicit_missing_runtime(self):
        catalog = {"yes": self.runtime, "no": replace(self.runtime, executable=Path("/nonexistent/toy-test"))}
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(run.select_runtimes(catalog, None), [self.runtime])
        with self.assertRaises(ValueError):
            run.select_runtimes(catalog, "no")

    def test_runtime_selection_and_overrides(self):
        selected = run.select_runtimes({"test": self.runtime}, "test",
                                       [f"test={sys.executable}"], [f"test={run.ROOT}"])
        self.assertEqual(selected[0].executable, Path(sys.executable).resolve())
        self.assertEqual(selected[0].cwd, run.ROOT)
        for names in ("unknown", "test,test", "test,", ""):
            with self.subTest(names=names), self.assertRaises(ValueError):
                run.select_runtimes({"test": self.runtime}, names)
        for overrides in (["test"], ["test="], ["unknown=/bin/sh"], ["test=/bin/sh", "test=/bin/sh"]):
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                run.select_runtimes({"test": self.runtime}, "test", overrides)

    def test_command_shapes(self):
        catalog = run.runtimes()
        self.assertEqual(catalog["toy"].command("arithmetic")[-2:], ["--", "arithmetic"])
        self.assertEqual(catalog["joy"].command("dispatch")[1], "-l")
        for workload in ("startup", "arithmetic", "log-fixed"):
            self.assertEqual(catalog["node-jitless"].command(workload)[1], "--jitless")
        self.assertEqual(catalog["toy"].command("log-fixed")[-2], "--")

    def test_cli_json_and_invalid_runs(self):
        bad = subprocess.run([sys.executable, str(run.SOURCE / "run.py"), "--runs", "0"], capture_output=True)
        self.assertNotEqual(bad.returncode, 0)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "results.json"
            subprocess.run([sys.executable, str(run.SOURCE / "run.py"), "--runs", "1",
                            "--no-warmup", "--runtimes", "python", "--output", str(output),
                            "startup", "string"], capture_output=True, check=True)
            results = json.loads(output.read_text())
        self.assertEqual(results["schema_version"], 1)
        self.assertEqual(len(results["process_ms"]["startup"]["Python"]), 1)
        self.assertEqual(results["internal_ms"]["startup"]["Python"], [])
        self.assertGreater(results["internal_ms"]["string"]["Python"][0], 0)
        self.assertIn("sources_sha256", results["metadata"])


class LogReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.oracle = runpy.run_path(str(run.ROOT / "benchmarks/check-applications.py"))
        cls.runtimes = [runtime for name, runtime in run.runtimes().items()
                        if name in ("toy", "python", "node", "node-jitless") and runtime.executable.is_file()]

    def invoke(self, runtime, path):
        command = runtime.command("log-fixed")
        command[-1] = str(path)
        return subprocess.run([*command, "--report"], cwd=runtime.cwd, env=run.ENVIRONMENT,
                              capture_output=True, text=True, timeout=120)

    def check_report(self, output, groups):
        lines = output.splitlines()
        self.assertEqual(lines.pop(0), "route\trequests\terrors\tmean_ms\tmax_ms\tbytes")
        self.assertEqual([line.split("\t")[0] for line in lines], sorted(groups))
        for line in lines:
            route, count, errors, mean, maximum, size = line.split("\t")
            expected = groups[route]
            self.assertEqual([int(count), int(errors), int(maximum), int(size)],
                             [expected[i] for i in (0, 1, 3, 4)])
            self.assertTrue(math.isclose(float(mean), expected[2] / expected[0], rel_tol=1e-12))

    def test_reports_and_checksums(self):
        rng = random.Random(20260911)
        varied = "# independent input\n\n" + "\n".join(
            f" {rng.choice(['/a', '/A', '/two words', '/café', '/literal/{}'])}?v={i}\t"
            f"{rng.choice([100, 200, 399, 400, 404, 599])}\t{rng.randrange(1000)}\t"
            f"{rng.randrange(10000)} \r" for i in range(1024))
        cases = ["", varied, *(self.oracle["log_text"](*case) for case in run.LOG_CASES.values())]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.tsv"
            for text in cases:
                path.write_text(text, encoding="utf-8", newline="")
                groups = self.oracle["analyze"](text)
                for runtime in self.runtimes:
                    with self.subTest(runtime=runtime.name, bytes=len(text)):
                        result = self.invoke(runtime, path)
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.check_report(result.stdout, groups)
        for workload, case in run.LOG_CASES.items():
            self.assertEqual(str(self.oracle["log_checksum"](self.oracle["analyze"](
                self.oracle["log_text"](*case)))), run.EXPECTED[workload])

    def test_invalid_inputs(self):
        cases = ["/a\t200\t1", "a\t200\t1\t1", "\t200\t1\t1",
                 "/a\t99\t1\t1", "/a\t600\t1\t1", "/a\t200\t-1\t1",
                 "/a\t200\t1\t-1", "/a\t200x\t1\t1", "/a\t200\t1.5\t1"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.tsv"
            for text in cases:
                path.write_text(text, encoding="utf-8")
                for runtime in self.runtimes:
                    with self.subTest(runtime=runtime.name, text=text):
                        self.assertNotEqual(self.invoke(runtime, path).returncode, 0)


if __name__ == "__main__":
    unittest.main()
