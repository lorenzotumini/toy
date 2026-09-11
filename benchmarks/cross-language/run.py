#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
import os
import platform
import re
import runpy
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "benchmarks" / "cross-language"
BUILD = ROOT / "build" / "cross-language"
ENVIRONMENT = {"LC_ALL": "C", "PATH": os.defpath}

EXPECTED = {
    "arithmetic": "10000000",
    "dispatch": "10000000",
    "fibonacci": "2178309",
    "sequence": "200000",
    "string": "200000",
    "map-lookup": "74998500000",
}
MICRO_WORKLOADS = ["startup", *EXPECTED]
LOG_CASES = {"log-fixed": (32000, 16), "log-wide": (32000, 16000)}
EXPECTED.update({"log-fixed": "3175586984", "log-wide": "3691945368000"})
WORKLOADS = [*MICRO_WORKLOADS, *LOG_CASES]


@dataclass(frozen=True)
class Runtime:
    name: str
    executable: Path
    source: Path | None
    arguments: tuple[str, ...] = ()
    cases: frozenset[str] = frozenset(MICRO_WORKLOADS)
    cwd: Path = ROOT
    separator: bool = False
    startup_arguments: tuple[str, ...] | None = None
    internal_scale: float = 1.0
    case_source: str | None = None
    application_source: Path | None = None

    def command(self, workload):
        if workload == "startup":
            if self.startup_arguments is not None:
                return [str(self.executable), *self.startup_arguments]
            return [str(self.executable), *self.arguments, "/dev/null"]
        if workload in LOG_CASES:
            if self.application_source is None:
                raise ValueError(f"{self.name} has no application source")
            separator = ["--"] if self.separator else []
            return [str(self.executable), *self.arguments, str(self.application_source),
                    *separator, str(BUILD / "fixtures" / f"{workload}.tsv")]
        if self.source is None:
            if self.case_source is None:
                raise ValueError(f"{self.name} has no source for {workload}")
            source = SOURCE / self.case_source.format(workload=workload)
            return [str(self.executable), *self.arguments, str(source)]
        separator = ["--"] if self.separator else []
        return [
            str(self.executable),
            *self.arguments,
            str(self.source),
            *separator,
            workload,
        ]


def runtimes():
    def installed(name):
        return Path(shutil.which(name) or f"/nonexistent/{name}")

    joy_cases = frozenset(
        {"startup", "arithmetic", "dispatch", "fibonacci", "sequence", "string"}
    )
    return {
        "toy": Runtime(
            "Toy",
            ROOT / "build" / "gcc" / "release" / "toy",
            SOURCE / "toy.toy",
            ("--file",),
            separator=True,
            internal_scale=1000.0,
            cases=frozenset(WORKLOADS),
            application_source=SOURCE / "log-report.toy",
        ),
        "joy0": Runtime(
            "Joy0",
            BUILD / "tools" / "joy0" / "joy",
            None,
            cases=joy_cases,
            cwd=BUILD / "tools" / "joy0",
            internal_scale=0.001,
            case_source="joy/{workload}.joy",
        ),
        "joy": Runtime(
            "Joy current",
            BUILD / "tools" / "joy" / "joy",
            None,
            ("-l",),
            joy_cases,
            BUILD / "tools" / "joy",
            internal_scale=1.0,
            case_source="joy/{workload}.joy",
        ),
        "gforth": Runtime(
            "Gforth",
            installed("gforth"),
            None,
            cases=frozenset({"startup", "arithmetic", "dispatch", "fibonacci"}),
            startup_arguments=("/dev/null", "-e", "bye"),
            internal_scale=0.001,
            case_source="gforth/{workload}.fs",
        ),
        "lua": Runtime(
            "Lua",
            installed("lua"),
            SOURCE / "lua.lua",
            internal_scale=0.000001,
        ),
        "luajit": Runtime(
            "LuaJIT",
            installed("luajit"),
            SOURCE / "lua.lua",
            internal_scale=0.000001,
        ),
        "janet": Runtime(
            "Janet",
            installed("janet"),
            SOURCE / "janet.janet",
            internal_scale=1000.0,
        ),
        "python": Runtime(
            "Python",
            Path(sys.executable),
            SOURCE / "python.py",
            internal_scale=0.000001,
            cases=frozenset(WORKLOADS),
            application_source=SOURCE / "log-report.py",
        ),
        "bun": Runtime(
            "Bun",
            installed("bun"),
            SOURCE / "javascript.js",
            ("run",),
            startup_arguments=("run", str(SOURCE / "empty.js")),
            internal_scale=0.001,
            cases=frozenset(WORKLOADS),
            application_source=SOURCE / "log-report.js",
        ),
        "node": Runtime(
            "Node",
            installed("node"),
            SOURCE / "javascript.js",
            startup_arguments=(str(SOURCE / "empty.js"),),
            internal_scale=0.001,
            cases=frozenset(WORKLOADS),
            application_source=SOURCE / "log-report.js",
        ),
        "node-jitless": Runtime(
            "Node --jitless",
            installed("node"),
            SOURCE / "javascript.js",
            ("--jitless",),
            startup_arguments=("--jitless", str(SOURCE / "empty.js")),
            internal_scale=0.001,
            cases=frozenset(WORKLOADS),
            application_source=SOURCE / "log-report.js",
        ),
    }


def select_runtimes(catalog, requested, executables=(), directories=()):
    for overrides, field in ((executables, "executable"), (directories, "cwd")):
        seen = set()
        for override in overrides:
            name, separator, value = override.partition("=")
            if not separator or not value or name not in catalog or name in seen:
                raise ValueError(f"invalid or duplicate {field} override: {override}")
            seen.add(name)
            catalog[name] = replace(catalog[name], **{field: Path(value).resolve()})
    names = requested.split(",") if requested is not None else list(catalog)
    if len(set(names)) != len(names) or any(name not in catalog for name in names):
        raise ValueError(f"invalid runtime selection: {','.join(names)}")
    selected = []
    for name in names:
        runtime = catalog[name]
        if not runtime.executable.is_file() or not os.access(runtime.executable, os.X_OK):
            message = f"missing {name} executable: {runtime.executable}"
            if requested:
                raise ValueError(message)
            print(f"skip {message}", file=sys.stderr)
            continue
        if not runtime.cwd.is_dir():
            raise ValueError(f"missing {name} directory: {runtime.cwd}; use --cwd {name}=PATH")
        selected.append(runtime)
    if not selected:
        raise ValueError("no available runtimes")
    return selected


def parse_internal_time(runtime, workload, stdout):
    # Joy may print banners, but the only numeric lines must be the exact
    # checksum followed by a finite, nonnegative duration. Accept exponent
    # notation in timers without weakening integer checksum validation.
    numeric = [line.strip() for line in stdout.splitlines()
               if re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", line.strip())]
    if len(numeric) != 2 or numeric[0] != EXPECTED[workload]:
        raise ValueError(f"expected checksum {EXPECTED[workload]} followed by one timer")
    internal_ms = float(numeric[1]) * runtime.internal_scale
    if not math.isfinite(internal_ms) or internal_ms < 0:
        raise ValueError("invalid internal time")
    return internal_ms


def execute(runtime, workload):
    started = time.perf_counter_ns()
    completed = subprocess.run(
        runtime.command(workload),
        cwd=runtime.cwd,
        capture_output=True,
        text=True,
        timeout=120,
        env=ENVIRONMENT,
    )
    elapsed_ms = (time.perf_counter_ns() - started) / 1_000_000
    if completed.returncode != 0:
        raise RuntimeError(
            f"{runtime.name} {workload} failed ({completed.returncode})\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    internal_ms = None
    if workload != "startup":
        try:
            internal_ms = parse_internal_time(runtime, workload, completed.stdout)
        except ValueError as error:
            raise RuntimeError(
                f"{runtime.name} {workload}: {error}\n"
                f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
            ) from error
    return elapsed_ms, internal_ms


def format_ms(value):
    if value is None:
        return "—"
    if value < 10:
        return f"{value:.2f}"
    if value < 100:
        return f"{value:.1f}"
    return f"{value:.0f}"


def stage_mounted_executables(all_runtimes, directory):
    staged = []
    for index, runtime in enumerate(all_runtimes):
        executable = runtime.executable.resolve()
        if not str(executable).startswith("/mnt/"):
            staged.append(runtime)
            continue
        target = directory / f"{index}-{executable.name}"
        shutil.copy2(executable, target)
        staged.append(replace(runtime, executable=target))
    return staged


def main():
    parser = argparse.ArgumentParser(description="Run the cross-language benchmark matrix")
    parser.add_argument("--runs", type=int, default=5, help="measured processes per cell")
    parser.add_argument("--no-warmup", action="store_true", help="skip one discarded process per cell")
    parser.add_argument("--runtimes", help="comma-separated runtime IDs (default: all available); "
                        + ", ".join(runtimes()))
    parser.add_argument("--executable", action="append", default=[], metavar="ID=PATH")
    parser.add_argument("--cwd", action="append", default=[], metavar="ID=PATH",
                        help="override a runtime's working directory (e.g. a Joy checkout)")
    parser.add_argument("--output", type=Path, help="write raw samples and reproducibility metadata as JSON")
    parser.add_argument("workloads", nargs="*", metavar="WORKLOAD", help=", ".join(WORKLOADS))
    args = parser.parse_args()
    if args.runs < 1:
        parser.error("--runs must be positive")

    selected = args.workloads or WORKLOADS
    if len(set(selected)) != len(selected) or any(workload not in WORKLOADS for workload in selected):
        parser.error("workloads must be distinct members of: " + ", ".join(WORKLOADS))
    try:
        all_runtimes = select_runtimes(runtimes(), args.runtimes, args.executable, args.cwd)
    except ValueError as error:
        parser.error(str(error))
    for workload in selected:
        if not any(workload in runtime.cases for runtime in all_runtimes):
            parser.error(f"none of the selected runtimes supports {workload}")
    prepare_fixtures(selected)
    metadata = describe_run(all_runtimes, selected, args)
    temporary = tempfile.TemporaryDirectory(prefix="toy-cross-language-")
    all_runtimes = stage_mounted_executables(all_runtimes, Path(temporary.name))
    metadata["executed_commands"] = {
        runtime.name: {workload: runtime.command(workload) for workload in selected if workload in runtime.cases}
        for runtime in all_runtimes
    }

    process_samples = {
        workload: {runtime.name: [] for runtime in all_runtimes}
        for workload in selected
    }
    internal_samples = {
        workload: {runtime.name: [] for runtime in all_runtimes}
        for workload in selected
    }
    for workload in selected:
        available = [runtime for runtime in all_runtimes if workload in runtime.cases]
        if not args.no_warmup:
            for runtime in available:
                print(f"warmup {workload}: {runtime.name}", file=sys.stderr)
                execute(runtime, workload)
        for run in range(args.runs):
            offset = run % len(available)
            order = available[offset:] + available[:offset]
            if run % 2:
                order.reverse()
            for runtime in order:
                process_ms, internal_ms = execute(runtime, workload)
                process_samples[workload][runtime.name].append(process_ms)
                if internal_ms is not None:
                    internal_samples[workload][runtime.name].append(internal_ms)
                print(
                    f"run {run + 1}/{args.runs} {workload}: "
                    f"{runtime.name} {process_ms:.3f} ms"
                    + (f" ({internal_ms:.3f} ms internal)" if internal_ms is not None else ""),
                    file=sys.stderr,
                )

    names = [runtime.name for runtime in all_runtimes]
    print("Process wall-time medians (ms):")
    print("| Workload | " + " | ".join(names) + " |")
    print("| --- | " + " | ".join("---:" for _ in names) + " |")
    for workload in selected:
        medians = []
        for name in names:
            values = process_samples[workload][name]
            medians.append(statistics.median(values) if values else None)
        print(
            f"| {workload} | "
            + " | ".join(format_ms(value) for value in medians)
            + " |"
        )

    timed = [workload for workload in selected if workload != "startup"]
    if timed:
        print("\nIn-program CPU-time medians (ms):")
        print("| Workload | " + " | ".join(names) + " |")
        print("| --- | " + " | ".join("---:" for _ in names) + " |")
        for workload in timed:
            medians = []
            for name in names:
                values = internal_samples[workload][name]
                medians.append(statistics.median(values) if values else None)
            print(
                f"| {workload} | "
                + " | ".join(format_ms(value) for value in medians)
                + " |"
            )
    temporary.cleanup()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps({
            "schema_version": 1,
            "metadata": metadata,
            "process_ms": process_samples,
            "internal_ms": internal_samples,
        }, indent=2) + "\n")


def describe_run(all_runtimes, workloads, args):
    def revision(directory):
        if not (directory / ".git").exists():
            return None
        return subprocess.check_output(["git", "-C", str(directory), "rev-parse", "HEAD"], text=True).strip()

    def sha256(path):
        with path.open("rb") as source:
            return hashlib.file_digest(source, "sha256").hexdigest()

    cpu_info = Path("/proc/cpuinfo")
    cpu = next((line.split(":", 1)[1].strip() for line in cpu_info.read_text().splitlines()
                if line.startswith("model name")), "unknown") if cpu_info.exists() else platform.processor()
    return {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "cpu": cpu,
        "cpu_affinity": sorted(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None,
        "driver_python": sys.version,
        "toy_commit": revision(ROOT),
        "toy_status": subprocess.check_output(["git", "-C", str(ROOT), "status", "--short"], text=True),
        "runs": args.runs,
        "discarded_processes_per_cell": 0 if args.no_warmup else 1,
        "jit_policy": "fresh process; first workload invocation, including tiering; no in-process warmup",
        "order": "rotate by run index, reverse odd runs; workloads in requested order",
        "environment": ENVIRONMENT,
        "workloads": workloads,
        "expected": {workload: EXPECTED[workload] for workload in workloads if workload in EXPECTED},
        "fixtures_sha256": {
            workload: sha256(BUILD / "fixtures" / f"{workload}.tsv")
            for workload in workloads if workload in LOG_CASES
        },
        "application_sources_sha256": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in [ROOT / "benchmarks/check-applications.py",
                         *sorted((ROOT / "examples/log-report/logs").glob("*.toy"))]
        },
        "sources_sha256": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in sorted(SOURCE.rglob("*"))
            if path.is_file() and path.suffix in {".py", ".toy", ".joy", ".js", ".lua", ".janet", ".fs"}
        },
        "runtimes": [{
            "name": runtime.name,
            "executable": str(runtime.executable.resolve()),
            "executable_sha256": sha256(runtime.executable),
            "cwd": str(runtime.cwd),
            "cwd_commit": revision(runtime.cwd),
            "internal_ms_per_unit": runtime.internal_scale,
        } for runtime in all_runtimes],
    }


def prepare_fixtures(workloads):
    selected = [workload for workload in workloads if workload in LOG_CASES]
    if not selected:
        return
    # Reuse the independently checked input generator, never its implementation
    # of the application inside a timed process. No fixture work is timed.
    oracle = runpy.run_path(str(ROOT / "benchmarks/check-applications.py"))
    directory = BUILD / "fixtures"
    directory.mkdir(parents=True, exist_ok=True)
    for workload in selected:
        source = oracle["log_text"](*LOG_CASES[workload])
        expected = oracle["log_checksum"](oracle["analyze"](source))
        if str(expected) != EXPECTED[workload]:
            raise ValueError(f"fixture checksum changed for {workload}")
        (directory / f"{workload}.tsv").write_text(source, encoding="utf-8", newline="")


if __name__ == "__main__":
    main()
