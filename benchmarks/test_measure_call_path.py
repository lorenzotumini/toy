"""Run with: python3 -B -m unittest discover -s benchmarks -p 'test_*.py' -v"""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    "measure_call_path", Path(__file__).with_name("measure-call-path.py"))
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def valid_output():
    return "\n".join(f"call-path case={case} elapsed_ns=1000000 checksum={checksum}"
                     for case, checksum in runner.EXPECTED.items()) + "\n"


class CallPathTests(unittest.TestCase):
    def test_complete_checked_output(self):
        phases = runner.parse_phases(valid_output())
        self.assertEqual(phases, dict.fromkeys(runner.EXPECTED, 1.0))

    def test_reject_incomplete_duplicate_or_extra_cases(self):
        output = valid_output()
        invalid = ("", output.split("\n", 1)[1], output + output.splitlines()[0],
                   output.replace("case=inline", "case=unknown"), output + "banner\n")
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(ValueError):
                runner.parse_phases(value)

    def test_reject_wrong_checksum_and_invalid_timings(self):
        output = valid_output()
        invalid = [output.replace("checksum=5000000", "checksum=42", 1)]
        invalid += [output.replace("elapsed_ns=1000000", f"elapsed_ns={value}", 1)
                    for value in ("0", "-1", "nan", "1.5", "inf")]
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(ValueError):
                runner.parse_phases(value)

    def test_reject_missing_extra_and_duplicate_fields(self):
        output = valid_output()
        invalid = (output.replace(" elapsed_ns=1000000", "", 1),
                   output.replace("call-path", "call-path extra=1", 1),
                   output.replace("case=inline", "case=inline case=inline", 1))
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(ValueError):
                runner.parse_phases(value)

    def test_sample_rejects_stderr(self):
        result = subprocess.CompletedProcess([], 0, valid_output(), "warning")
        with patch.object(runner.subprocess, "run", return_value=result):
            with self.assertRaises(ValueError):
                runner.sample(Path("toy"))

    def test_sample_checks_subprocess_and_units(self):
        result = subprocess.CompletedProcess([], 0, valid_output(), "")
        with patch.object(runner.subprocess, "run", return_value=result) as invoke:
            phases = runner.sample(Path("toy"))
        self.assertEqual(phases["inline"], 1.0)
        self.assertGreater(phases["process"], 0)
        self.assertTrue(invoke.call_args.kwargs["check"])
        self.assertEqual(invoke.call_args.kwargs["timeout"], 120)
        self.assertEqual(invoke.call_args.args[0][-1], str(runner.SOURCE))

    def test_cli_alternates_pairs_and_records_raw_samples(self):
        calls = []

        def sample(executable):
            calls.append(executable.name)
            return dict.fromkeys([*runner.EXPECTED, "process"],
                                 2.0 if executable.name == "candidate" else 4.0)

        with tempfile.TemporaryDirectory() as directory:
            baseline = Path(directory) / "baseline"
            candidate = Path(directory) / "candidate"
            baseline.write_bytes(b"baseline executable fixture")
            candidate.write_bytes(b"candidate executable fixture")
            output = Path(directory) / "results.json"
            arguments = ["measure-call-path.py", "--baseline", str(baseline),
                         "--toy", str(candidate), "--runs", "3", "--output", str(output)]
            with patch.object(sys, "argv", arguments), patch.object(runner, "sample", sample):
                with contextlib.redirect_stdout(io.StringIO()):
                    runner.main()
            data = json.loads(output.read_text())
        self.assertEqual(calls, ["baseline", "candidate", "baseline", "candidate",
                                 "candidate", "baseline", "baseline", "candidate"])
        self.assertEqual(len(data["samples"]), 3)
        self.assertEqual(data["warmups_per_executable"], 1)
        self.assertEqual(data["summaries"][0]["median_paired_ratio"], 0.5)
        self.assertEqual(len(data["source_sha256"]), 64)
        self.assertEqual(len(data["executables"]["baseline"]["sha256"]), 64)

    def test_reject_nonpositive_runs(self):
        for runs in ("0", "-1"):
            with patch.object(sys, "argv", ["measure-call-path.py", "--baseline", "toy",
                                            "--runs", runs]):
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    runner.main()


if __name__ == "__main__":
    unittest.main()
