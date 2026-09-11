# Cross-language benchmarks

This optional Linux matrix reports fresh-process wall time and in-program CPU
time separately, validates every timed result, and saves raw samples. It is a
set of reference points, **not a single language ranking**. Python 3.11+ is
required for the runner; no third-party Python packages are needed.

## Candidates

- [Joy0](https://github.com/Wodan58/joy0) and
  [current Joy](https://github.com/Wodan58/Joy): the closest language-model
  comparisons, with quotations, combinators, and a data stack. They do not
  promise the same collection, ownership, capture, or debugging semantics.
- CPython and Node.js: practical general-purpose scripting references.
- Lua: a small, mature non-JIT VM reference. LuaJIT is a separate configuration,
  not a faster build of the same Lua release.
- `node-jitless`: Node with `--jitless`, alongside ordinary Node. This controls
  one important execution-mode difference without making the two languages or
  their native primitives identical.
- Optional Janet, Bun, and Gforth adapters remain available. Gforth only runs
  scalar/control tests: unboxed cells and threaded execution make it a
  lower-level reference, not a peer collection runtime.

## Workloads and interpretation

| Workload | Work performed | Important qualification |
| --- | --- | --- |
| `arithmetic` | Ten million integer increments | JITs may specialize the loop. |
| `dispatch` | Ten million user-defined increment calls | JITs may inline the call; this does not measure surviving machine-level calls. |
| `fibonacci` | Naive recursive Fibonacci(32); `binrec` in Toy/Joy | A recursion/combinator stress test, not the best Fibonacci algorithm. |
| `sequence` | Ten builds and interpreted sums of 20,000 ones | Joy cons lists versus growable arrays; no native `sum` or bulk fill shortcut. |
| `string` | Twenty incremental builds of 10,000-character strings | Joy string `cons` copies the growing string: quadratic versus amortized-linear Toy append or fragment-and-join builders. Not an equal-complexity VM comparison. |
| `map-lookup` | 50,000 integer entries, one million lookups | Includes construction and loop overhead. Lua's dense integers can use array storage; this is not a general hash-table ranking. Joy/Gforth omitted. |
| `log-fixed` | Parse, validate, aggregate, sort, and render 32,000 TSV records / 16 routes | Repeated string-key updates; actual Toy log-report example. |
| `log-wide` | Same pipeline / 16,000 routes | More distinct keys, allocation, sorting, and output. |
| `startup` | Fresh process reading an empty file | Includes process launch and configured initialization, not pure VM initialization. |

Log cases use the actual `examples/log-report/logs` package and idiomatic
Python/JavaScript ports. All validate field counts, routes, decimal numbers,
status ranges, and nonnegative counters. Ports may mutate private group records;
Toy uses its existing value/ownership model. No intermediate snapshots are
observable. Numeric inputs and checksums fit exactly in JavaScript Numbers.
These are comparable applications on the fixture domain, not implementations
of all Unicode, overflow, or formatting edge cases of one another's languages.
Reports are checked field-by-field, including sorting and numeric means, rather
than requiring identical floating-point text formatting.

The runner creates identical fixture bytes outside all measured processes using
the existing independent application oracle. In-program log time includes
analysis and report construction, but excludes source/package loading, file
reading, checksum computation, and output. Process wall time includes those
costs. Microbenchmark CPU timers wrap the workload; Joy additionally prints
its checksum before stopping its timer. Joy0's clock uses Linux clock ticks
(microseconds), whereas current Joy's clock has millisecond granularity.

Each sample is a **fresh process, first workload invocation**. The discarded
process warms filesystem/code pages; it does not warm the measured process's
JIT. A long loop may tier up within one invocation. Node's process CPU timer
also includes background compiler threads, so CPU time can exceed wall time.
Do not infer warmed server throughput from these measurements. Timed JITs are
allowed to optimize the program; checksums ensure results are consumed but
cannot prove a particular instruction or call survived optimization.

## Setup and running

Build Toy with `./nob build`. The default executable is now the current
`build/gcc/release/toy`; standard runtimes are discovered through `PATH`, and
Python uses the runner's interpreter. Joy source and binaries live under the
ignored build directory, without installing libraries into the user's home:

```console
git clone https://github.com/Wodan58/joy0.git build/cross-language/tools/joy0
git clone https://github.com/Wodan58/Joy.git build/cross-language/tools/joy
make -C build/cross-language/tools/joy0 CC=gcc
make -C build/cross-language/tools/joy
```

Both upstream makefiles use `-O3`. Record/pin their Git revisions for durable
results; see the experiment reports for exact revisions. Joy0 requires
`sizeof(long) == sizeof(void *)`, satisfied by LP64 Linux, not 64-bit Windows.
Joy0 loads the checkout's `usrlib.joy`; current Joy runs with `-l` to disable
automatic user-library loading. These different startup configurations are
visible in process time, not presented as equivalent library startup.

Run the available matrix, or explicitly require a reproducible subset:

```console
python3 benchmarks/cross-language/run.py --runs 7
python3 benchmarks/cross-language/run.py --runs 7 \
  --runtimes toy,joy0,joy,lua,luajit,python,node,node-jitless \
  --output build/cross-language/results.json
python3 benchmarks/cross-language/run.py --runs 3 \
  --runtimes toy,python,node log-fixed log-wide
```

Missing optional runtimes are reported and skipped in automatic mode. Explicitly
requested missing runtimes, unknown names/workloads, and workloads supported by
none of the selected runtimes are errors. Unsupported individual cells are
shown as dashes, not zeros. Samples rotate and reverse runtime order between
rounds. JSON records raw samples, expected checksums, commands, executable and
source hashes, checkout commits, OS/CPU, affinity, and the timing policy. Record
runtime versions, build flags, and power state in the accompanying report.

Override paths without editing the runner:

```console
python3 benchmarks/cross-language/run.py --runtimes toy,joy0 \
  --executable toy=/path/to/toy --executable joy0=/path/to/joy0/joy \
  --cwd joy0=/path/to/joy0 arithmetic dispatch
```

As in the original harness, executables below WSL's `/mnt/` are copied into a
temporary native-Linux directory to avoid Windows-filesystem paging artifacts.
The original executable hashes and actual executed commands are both recorded.
Child environments contain only `LC_ALL=C` and a system `PATH`, preventing
personal runtime options, home libraries, and Python startup settings from
silently changing the test. This is an intentionally controlled configuration.

Correctness and runner tests (available Toy/Python/Node configurations):

```console
python3 -m unittest discover -s benchmarks/cross-language -v
```

Tests check both full application reports against the existing independent
oracle, randomized input, malformed records, checksum/timer rejection, runtime
selection, and JSON output. The main matrix validates checksums on every sample.
Other runtimes require their own successful matrix run; the tests do not install
or implicitly claim to cover missing adapters.

Dependencies remain outside the normal Nob build. Durable records:
[original August matrix](../results/2026-08-11-cross-language.md) and
[September refresh](../results/2026-09-11-cross-language.md). The machines differ;
do not treat a difference between those tables as a Toy optimization speedup.
