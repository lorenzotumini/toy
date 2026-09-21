#!/usr/bin/env python3
"""Paired wall-time measurements of checked call-path diagnostic phases."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import statistics
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "benchmarks/call-path.toy"
EXPECTED = {
    "inline": 5000000, "user-word": 5000000, "quotation-exec": 5000000,
    "symbol-exec": 5000000, "boolean-branch": 1000000,
    "predicate-branch": 1000000, "fib-word": 317811,
    "fib-predicate": 317811, "fib-binrec": 317811, "fold": 19999900000,
}


def parse_phases(output):
    """Validate every case and checksum before accepting its elapsed time."""
    phases = {}
    for line in output.splitlines():
        prefix, *tokens = line.split()
        if prefix != "call-path":
            raise ValueError(f"Unexpected output: {line!r}")
        fields = dict(token.split("=", 1) for token in tokens)
        if len(tokens) != 3 or set(fields) != {"case", "elapsed_ns", "checksum"}:
            raise ValueError(f"Unexpected fields: {line!r}")
        case = fields["case"]
        if case not in EXPECTED or case in phases or int(fields["checksum"]) != EXPECTED[case]:
            raise ValueError(f"Invalid case/checksum: {line!r}")
        duration = int(fields["elapsed_ns"])
        if duration <= 0:
            raise ValueError(f"Nonpositive timing: {line!r}")
        phases[case] = duration / 1e6
    if phases.keys() != EXPECTED.keys():
        raise ValueError("Missing call-path cases")
    return phases


def sample(executable):
    started = time.perf_counter_ns()
    result = subprocess.run([str(executable), "--file", str(SOURCE)], cwd=ROOT,
                            capture_output=True, text=True, check=True, timeout=120)
    elapsed = (time.perf_counter_ns() - started) / 1e6
    if result.stderr:
        raise ValueError(result.stderr)
    phases = parse_phases(result.stdout)
    return {**phases, "process": elapsed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--toy", type=Path, default=ROOT / "build/gcc/release/toy")
    parser.add_argument("--runs", type=int, default=7)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.runs < 1:
        parser.error("--runs must be positive")
    executables = {"baseline": args.baseline.resolve(), "candidate": args.toy.resolve()}
    for executable in executables.values():
        sample(executable)
    samples = []
    for index in range(args.runs):
        order = ["baseline", "candidate"] if index % 2 == 0 else ["candidate", "baseline"]
        samples.append({name: sample(executables[name]) for name in order})
    summaries = []
    print("| Case | Baseline ms | Candidate ms | Paired ratio |")
    print("| --- | ---: | ---: | ---: |")
    for case in [*EXPECTED, "process"]:
        baseline = [pair["baseline"][case] for pair in samples]
        candidate = [pair["candidate"][case] for pair in samples]
        row = {"case": case, "baseline_median_ms": statistics.median(baseline),
               "candidate_median_ms": statistics.median(candidate),
               "median_paired_ratio": statistics.median(b / a for a, b in zip(baseline, candidate))}
        summaries.append(row)
        print(f"| {case} | {row['baseline_median_ms']:.3f} | {row['candidate_median_ms']:.3f} "
              f"| {row['median_paired_ratio']:.4f} |")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps({
            "schema_version": 1, "recorded_utc": datetime.now(timezone.utc).isoformat(),
            "platform": platform.platform(), "runs": args.runs,
            "warmups_per_executable": 1,
            "timing": "wall time; fresh processes, alternating pair order, fixed phase order",
            "executables": {name: {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                            for name, path in executables.items()},
            "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            "expected": EXPECTED, "summaries": summaries, "samples": samples,
        }, indent=2) + "\n")


if __name__ == "__main__":
    main()
