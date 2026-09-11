# Experiment: Cross-language refresh with a checked application

- Date: 2026-09-11
- Toy: `7f84553616697ba04fcaded38ee21cc52589d6a7`, GCC Release
  (`-O3 -DNDEBUG`); no runtime or example implementation changes in this experiment.
- Joy0: `51414779a42d06c1c6aac2bf519c7deb72f96ad7`;
  current Joy: `fe9fa0fa7db714340dbe17aedaff77f926e7c78a`.
  Both built from their upstream makefiles with GCC and `-O3`;
  current Joy uses its default `-DNOBDW` copying-GC configuration.
- Compiler: GCC 16.2.1 20260810, verified in the Toy executable's `.comment`.
- OS / CPU: Arch Linux, Linux 7.2.3-arch1-3, x86-64 LP64 /
  Intel Core i9-11900K, 8 cores / 16 logical CPUs.
- Power state: `powersave` CPU-frequency governor, Intel turbo enabled;
  no fixed frequency or CPU pinning, affinity 0–15. No concurrent benchmark,
  build, or test jobs were deliberately run during measurement. Ordinary
  workstation background activity was not controlled.
- Installed runtimes: CPython 3.14.7 (distribution PGO/LTO build, experimental
  JIT disabled), Node v22.23.2, Lua 5.5.1, LuaJIT 2.1.1788460057.
  Node's same executable also runs with `--jitless`.
- Method: seven fresh processes per supported cell, one discarded process per
  cell, rotating/reversing runtime order. 62 cells, 434 retained samples,
  62 discarded warmups. Every sample passed its checksum check.
- Raw evidence: [matrix.json](2026-09-11-cross-language/matrix.json), including
  every sample, commands, executable/source/fixture hashes and checkout commits.
- Harness and interpretation details:
  [cross-language README](../cross-language/README.md).

## What existed, and what changed

The [August experiment](2026-08-11-cross-language.md) already covered most of
these languages. Its runner depended on the old sibling checkout layout and
specific WSL-staged binaries. It also predates the compact `times`, native
fast-path, and shared capture-stack improvements. That experiment ran on an
i7-1065G7 under WSL, so **the old and new absolute timings are not a measurement
of Toy's optimization speedup**. The two Joy revisions happen to be unchanged.

This refresh makes runtime selection and executable/working-directory paths
configurable, discovers installed runtimes through PATH, saves raw JSON, and
rejects invalid checksums/timers. It adds LuaJIT and JIT-disabled Node as
separately labelled configurations. Janet, Bun, and Gforth remain optional
adapters but were not installed or measured here.

It also adds two application cells using the existing Toy log-report package,
not a freshly optimized Toy port. Python and JavaScript ports perform the same
validated TSV analysis, string-key grouping, lexicographic route sorting, and
report generation. Both cases process 32,000 records; fixed cardinality uses
16 routes and wide cardinality uses 16,000. Fixture generation and reading are
outside in-program timing. All processes read identical UTF-8 bytes, including
mixed LF/CRLF endings. Fields and ordering in complete reports were independently
checked, including numeric means; float text need not be byte-identical.

## Results

In-program CPU-time medians, milliseconds (lower is better):

| Workload | Toy | Joy0 | Joy current | Lua | LuaJIT | Python | Node | Node --jitless |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Arithmetic | 104 | 77.4 | 146 | 30.9 | 8.93 | 249 | 6.32 | 85.2 |
| User-word/function calls | 219 | 101 | 230 | 152 | 8.22 | 373 | 6.69 | 200 |
| Recursive Fibonacci(32) | 573 | 142 | 303 | 96.8 | 11.3 | 164 | 16.5 | 133 |
| Sequence build + sum | 5.99 | 11.8 | 15.0 | 3.56 | 1.25 | 6.85 | 5.94 | 8.40 |
| String construction † | 2.67 | 187 | 253 | 3.04 | 1.48 | 4.10 | 4.67 | 6.02 |
| Dense-integer map workload ‡ | 58.6 | — | — | 4.90 | 1.04 | 48.0 | 20.3 | 40.4 |
| Log report: 16 routes | 45.7 | — | — | — | — | 70.4 | 24.5 | 41.6 |
| Log report: 16,000 routes | 61.4 | — | — | — | — | 80.8 | 48.5 | 62.0 |

Fresh-process wall-time medians, milliseconds:

| Workload | Toy | Joy0 | Joy current | Lua | LuaJIT | Python | Node | Node --jitless |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Startup | 0.48 | 0.45 | 0.38 | 0.40 | 0.47 | 7.40 | 14.2 | 13.3 |
| Arithmetic | 105 | 78.4 | 148 | 31.6 | 9.83 | 258 | 23.2 | 107 |
| User-word/function calls | 220 | 103 | 232 | 153 | 9.11 | 382 | 23.1 | 221 |
| Recursive Fibonacci(32) | 575 | 144 | 305 | 97.7 | 12.2 | 172 | 34.1 | 156 |
| Sequence build + sum | 6.65 | 12.6 | 16.0 | 4.25 | 1.93 | 14.6 | 20.5 | 29.4 |
| String construction † | 3.27 | 208 | 255 | 3.70 | 2.19 | 11.8 | 20.2 | 26.7 |
| Dense-integer map workload ‡ | 59.3 | — | — | 5.57 | 1.73 | 56.1 | 35.0 | 61.6 |
| Log report: 16 routes | 46.9 | — | — | — | — | 86.2 | 38.3 | 62.9 |
| Log report: 16,000 routes | 68.8 | — | — | — | — | 101 | 62.7 | 86.2 |

† Both Joy implementations allocate and copy the old string for every string
`cons` in this source. That is quadratic construction, unlike Toy's growable
string and the fragment-and-join ports. The large gap is a property of this
workload's implementation/representation, not evidence that Joy's VM is
70–95 times slower. This report does not claim the supplied Joy source is the
fastest possible Joy string builder. Source evidence:
[Joy0 cons](https://github.com/Wodan58/joy0/blob/51414779a42d06c1c6aac2bf519c7deb72f96ad7/interp.c#L591),
[current Joy cons](https://github.com/Wodan58/Joy/blob/fe9fa0fa7db714340dbe17aedaff77f926e7c78a/src/cons_swons.h).

‡ Lua/LuaJIT's dense integer keys can use table array storage, unlike the
general maps in the other ports. This row also includes table construction,
index arithmetic, and interpreter looping. It cannot isolate hash lookup cost.
The log application provides a more relevant mixed workload with string keys,
but does not isolate hashing either.

## Interpretation

1. **Toy is competitive on this text-processing application.** Its workload CPU
   time is 35% lower than the Python port for fixed routes and 24% lower for
   wide routes. Node uses less CPU: Toy takes 1.87× and 1.27× as long respectively.
   With process costs included, Toy takes only 1.23× and 1.10× Node's time.
   Against JIT-disabled Node, Toy's application CPU time is within about 10%
   on both cases. These results describe these checked ports and input shapes,
   not every Python/JS implementation of log analysis.
2. **Arithmetic is no longer a general indictment of Toy's interpreter.** Toy
   beats this CPython build on the arithmetic and call loops, and is faster
   than current Joy on arithmetic. On the call row Toy and current Joy are
   close enough that a 5% median difference is not a strong architectural
   conclusion. Original Joy0 remains faster on both.
3. **Recursion is the clearest remaining weak reference point.** Toy takes
   1.89× current Joy's CPU time, 4.03× Joy0's, 3.49× Python's, and 5.92× Lua's on
   `binrec` Fibonacci. This makes recursion-controller/frame work a worthwhile
   profiling target. It does not establish which internal mechanism accounts
   for the gap or justify a rewrite without Toy-local controlled experiments.
4. **Tiny calls still deserve investigation.** Within Toy, replacing inline
   increment with a user word adds about 115 ms across ten million iterations;
   within Joy0 the difference is about 24 ms. This is a useful call-path
   hypothesis, not a cross-language measurement of identical call semantics.
5. **JIT and non-JIT results answer different questions.** Default Node and
   LuaJIT are much faster on arithmetic and recursive computation. A trivial
   increment function may disappear through inlining, so their dispatch row
   is not a measurement of ten million surviving runtime calls. Node's
   JIT-disabled reference narrows some gaps substantially, but Toy remains
   much slower on the recursion stress test even against that configuration.

All samples are first workload invocations in fresh processes: this is a
short-lived script comparison, **not warmed steady-state throughput**. V8's
[JIT-less mode](https://v8.dev/blog/jitless) changes both JavaScript and regular
expression execution; the Node mode difference cannot all be assigned to user
function compilation. [Node's process CPU timer](https://nodejs.org/download/release/v22.23.2/docs/api/process.html#processcpuusagepreviousvalue)
counts CPU across threads, including background compilation, and need not equal
wall time. Joy0 auto-loads its checkout's user libraries; current Joy disables
automatic library loading. The sub-millisecond startup cells should not be
used to rank pure initialization costs.

### Variability and scope

Toy's CPU-time interquartile range divided by its median was 0.9–4.0% across
workloads. Application IQR/median was 2.3–4.0% across the four configurations;
individual outliers remain in the data (Python fixed-route maximum 82.6 ms
versus 70.4 ms median, Toy wide-route maximum 67.4 versus 61.4 ms). Some short
microbenchmarks varied more: LuaJIT arithmetic IQR/median was 17%, and
JIT-disabled Node sequence was 16%. Current Joy's integer-millisecond clock
further limits precision for small workloads. No samples were trimmed.

Coverage remains intentionally modest: synthetic ASCII numeric microbenchmarks
and one UTF-8 text application with controlled cardinality, not networking,
embedding, large external corpora, sustained services, float-heavy simulation,
or memory consumption. Full reports also pass separately generated non-ASCII
and mixed-case route tests, but those inputs are not timed. Next useful work
is a particle/float application port and explicit warmed in-process runs, not
an overall geometric-mean score from incompatible workloads.

## Reproduction and validation

Use the two upstream revisions listed above, and build them in the locations
documented in the harness README. No global install or home-library modification
is required. The final matrix command was:

```console
./nob build
python3 -m unittest discover -s benchmarks/cross-language -v
python3 benchmarks/cross-language/run.py --runs 7 \
  --runtimes toy,joy0,joy,lua,luajit,python,node,node-jitless \
  --output benchmarks/results/2026-09-11-cross-language/matrix.json
```

All eight runner/application tests passed. They cover full reports for both
32,000-record fixtures, empty and independently randomized input, nine malformed
record cases, and checksum/timer/configuration/JSON handling. Toy, Python,
Node, and Node `--jitless` were all present for those integration checks.
The matrix additionally validated every Joy/Lua/LuaJIT microbenchmark result.
No runtime source, builtin metadata, capture behavior, or installed SDK content
was changed; runtime-wide sanitizer tests were not rerun for this tooling-only
experiment.
