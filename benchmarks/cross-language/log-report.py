"""Idiomatic port of examples/log-report: validated TSV -> grouped, sorted TSV."""

from pathlib import Path
import re
import sys
import time


def integer(text):
    text = text.strip()
    if re.fullmatch(r"[+-]?[0-9]+", text) is None:
        raise ValueError("expected decimal integer")
    return int(text)


def analyze(text):
    groups = {}
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 4:
            raise ValueError("expected four tab-separated fields")
        route = fields[0].strip().split("?", 1)[0]
        if not route.startswith("/"):
            raise ValueError("route must start with /")
        status, latency, size = (integer(value) for value in fields[1:])
        if not 100 <= status <= 599 or latency < 0 or size < 0:
            raise ValueError("invalid status, latency, or byte count")
        stats = groups.get(route)
        if stats is None:
            stats = groups[route] = [0, 0, 0, 0, 0]
        stats[0] += 1
        stats[1] += status >= 400
        stats[2] += latency
        stats[3] = max(stats[3], latency)
        stats[4] += size
    return groups


def report(groups):
    lines = ["route\trequests\terrors\tmean_ms\tmax_ms\tbytes"]
    for route in sorted(groups):
        count, errors, total, maximum, size = groups[route]
        lines.append(f"{route}\t{count}\t{errors}\t{total / count}\t{maximum}\t{size}")
    return "\n".join(lines) + "\n"


def checksum(groups):
    return sum((int(route.rsplit("/", 1)[1]) + 1) *
               (count * 3 + errors * 5 + total * 7 + maximum * 11 + size * 13)
               for route, (count, errors, total, maximum, size) in groups.items())


def main():
    # Decode identical bytes without Python's universal-newline conversion.
    text = Path(sys.argv[1]).read_bytes().decode("utf-8")
    started = time.process_time_ns()
    groups = analyze(text)
    output = report(groups)
    elapsed = time.process_time_ns() - started
    if len(sys.argv) > 2:
        print(output, end="")
    else:
        print(checksum(groups))
        print(elapsed)


if __name__ == "__main__":
    main()
