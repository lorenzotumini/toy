# Graph Report - toy  (2026-09-21)

## Corpus Check
- 251 files · ~301,099 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 182 file(s) not represented in the graph (top: .toy 139, .stderr 10, (none) 7)

## Summary
- 2947 nodes · 9969 edges · 117 communities (107 shown, 10 thin omitted)
- Extraction: 75% EXTRACTED · 25% INFERRED · 0% AMBIGUOUS · INFERRED: 2461 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Control Word Builtins
- Object Runtime Core
- Dispatch Performance Experiments
- Packages and Word Lookup
- Nob Build System
- Bindgen Test Suite
- FFI Extension API
- Windows Line Editing
- POSIX Line Editing
- Data Builtins
- Meta Builtins and Hints
- Core Numeric Builtins
- Public API Layer
- Builtin Generation Tools
- Sequence Operations
- Test Support Headers
- REPL Runtime
- SQLite Extension
- Toy Public Headers
- CLI Entry Point
- Debug Adapter Protocol
- Nob Library API
- Toy Parser
- Embedding API Tests
- Go Source Analysis
- Debug Session Runner
- LSP Protocol Types
- Tree-sitter Node Binding
- Bindgen C Fixtures
- Benchmark Experiment Notes
- Nob Command Runner
- Debug Inspector
- Embedding Examples
- IO Format Builtins
- Go Formatter Config
- Go Source Lexer
- Go Formatter CLI
- Debug Protocol
- LSP Resolution Cache
- LSP Server Handlers
- Debug Control
- Nob Windows Shim
- System Builtins
- LSP Document Store
- LSP Test Suite
- Project Documentation
- Go SDK Tool
- Random and Locking
- Go CLI Formatter
- TextMate Grammar
- Go Formatter Tests
- Cross-language Run Harness
- Benchmark Comparison Library
- Tree-sitter Config
- Go LSP Indexer
- Measurement Scripts
- Benchmark Test Scripts
- Embedding Capture Tests
- User Reference Docs
- Debug Printing
- Native Plugin Tests
- Application Oracles
- Embedding Experiment Notes
- C Interop Docs
- JavaScript Benchmark Workloads
- Log Report JavaScript
- Native Library Loader
- Go LSP Analysis
- Builtin Registry
- LSP Index Tests
- Tree-sitter Grammar
- Data Layout Experiments
- Call Path Tests
- FFI Fixtures
- LSP Builtin Docs
- Log Report Python
- Tree-sitter Go Bindings
- Tree-sitter Grammar Spec
- Python Benchmark Workloads
- Capture Stack Experiments
- Deferred Call Example
- Allocation Statistics
- Tree-sitter Grammar
- Lua Benchmark Workloads
- Cross-language Runner Tests
- Call Path Experiments
- Nob String Builder
- Natural Sort
- Core Package Docs
- Tree-sitter Toy Parser
- Native Fast Path Experiments
- Tree-sitter Grammar
- Log Report Tests
- Nob Log Handlers
- Nob Process Helpers
- Builtin Word Lists
- Install Scripts
- Tree-sitter Grammar
- Tree-sitter Grammar
- Tree-sitter Grammar
- Tree-sitter Grammar
- Tree-sitter Grammar
- Tree-sitter Grammar
- Tree-sitter Grammar
- Tree-sitter Grammar
- Tree-sitter Grammar
- Tree-sitter Grammar
- Tree-sitter Grammar
- Tree-sitter Grammar
- Tree-sitter Grammar
- Tree-sitter Grammar
- Filter Reserve Experiments
- Go Tools Module

## God Nodes (most connected - your core abstractions)
1. `tf_obj_release()` - 203 edges
2. `tf_stack_push()` - 162 edges
3. `tf_stack_pop()` - 139 edges
4. `tf_obj_typeof()` - 122 edges
5. `tf_ctx_runtime_errorf()` - 111 edges
6. `tf_stack_peek()` - 110 edges
7. `tf_ctx_require_stack()` - 77 edges
8. `tf_ctx_require_type()` - 69 edges
9. `tf_obj_retain()` - 63 edges
10. `tf_xmalloc()` - 62 edges

## Surprising Connections (you probably didn't know these)
- `Quickened common instructions (dup, pred, +, *, <)` --conceptually_related_to--> `quickened_call_dispatch()`  [INFERRED]
  benchmarks/results/2026-07-21-quickened-instructions.md → src/tf_exec.c
- `Cross-language Reference Set (Joy, Lua, Python, Node, Janet, Gforth)` --semantically_similar_to--> `Toy Language Overview`  [INFERRED] [semantically similar]
  benchmarks/cross-language/README.md → README.md
- `Embedding Toy in C` --references--> `toy_push_resource()`  [EXTRACTED]
  docs/embedding.md → include/toy.h
- `Embedding Toy in C` --references--> `toy_defer_call()`  [EXTRACTED]
  docs/embedding.md → include/toy.h
- `Associative quick-program cache` --conceptually_related_to--> `quick_program_set()`  [INFERRED]
  benchmarks/results/2026-08-10-associative-program-cache.md → src/tf_exec.c

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **C Interop Routes** — c_interop_ffi, c_interop_generated_bindings, c_interop_handwritten_extensions, docs_embedding_toy_state [EXTRACTED 1.00]
- **Toy Value Semantics** — docs_data_model_symbol_call_distinction, runtime_collection_layouts, runtime_tagged_integers, runtime_capture_binding_stack [INFERRED 0.85]
- **Development Measurement Stack** — nob_build_modes, docs_development_observability_modes, test_file_conventions, docs_roadmap_performance_track [INFERRED 0.85]
- **C Extension Example Packages** — examples_packages_basic_readme, examples_packages_bindgen_readme, examples_packages_raylib_readme, examples_packages_sqlite_readme [EXTRACTED 1.00]
- **Runnable Consumer Applications** — examples_log_report_readme, examples_particles_readme, examples_graphs_readme, examples_embedding_readme [INFERRED 0.85]
- **Control-State Storage Experiments** — binrec_inline_snapshot, control_inline_snapshots, frame_scratch_arena, compact_recursion_controllers [INFERRED 0.85]
- **Word Dispatch Optimization Experiments** — word_lookup_cache_v1, retained_word_resolution_cache, quickened_instructions, dispatch_rejection_criteria [INFERRED 0.85]
- **Rejected Performance Prototypes** — call_path_rejected_prototypes, state_isolation_rejected_sync, dispatch_rejection_criteria, bytecode_sidecar_prototype [INFERRED 0.85]

## Communities (117 total, 10 thin omitted)

### Community 0 - "Control Word Builtins"
Cohesion: 0.07
Nodes (129): binrec_state, bytebuf, merge_state, predicate_eval, app2_cleanup(), app2_step(), bi_cleanup(), bi_step() (+121 more)

### Community 1 - "Object Runtime Core"
Cohesion: 0.05
Nodes (120): obj_writer, tf_xrealloc(), format_buffer_write(), FILE, tf_obj, tf_obj_write_fn, deque_ensure_capacity(), deque_slot() (+112 more)

### Community 2 - "Dispatch Performance Experiments"
Cohesion: 0.06
Nodes (94): Associative quick-program cache, Experiment: Inline binrec rollback snapshots, Experiment: Shared inline control-stack snapshots, Experiment: Frame-owned scratch arena, Experiment: Quickened call instructions, Experiment: Associative quick-program cache, Inline rollback snapshot in binrec state, 32-pointer inline snapshots for cached control states (+86 more)

### Community 3 - "Packages and Word Lookup"
Cohesion: 0.06
Nodes (91): Experiment: Resolved word lookup cache, Experiment: Retained word-resolution cache, dirent, package_decl_kind, package_manifest, package_scan, Generation-guarded retained word-resolution cache, append_executable_directory() (+83 more)

### Community 4 - "Nob Build System"
Cohesion: 0.09
Nodes (90): Build_Mode, Compiler, main(), Package_Test_Case, Proc, Procs, String_Builder, build_c_benchmark() (+82 more)

### Community 5 - "Bindgen Test Suite"
Cohesion: 0.06
Nodes (89): ref_assert, assert, badHeader, dependentManifest, dependentRendered, detailedRendered, detailedStatus, duplicateResource (+81 more)

### Community 6 - "FFI Extension API"
Cohesion: 0.05
Nodes (83): Color, toy_extension_api, TOY_EXTENSION_EXPORT, toy_state, toy_status, copy_string(), destroy_function(), destroy_library() (+75 more)

### Community 7 - "Windows Line Editing"
Cohesion: 0.06
Nodes (76): abAppend(), abFree(), abInit(), acceptCompletion(), acceptDisplayedCompletion(), addHistoryPlaceholder(), ansiEscapeLen(), linenoiseCompletionCallback (+68 more)

### Community 8 - "POSIX Line Editing"
Cohesion: 0.06
Nodes (73): abAppend(), abFree(), abInit(), acceptCompletion(), addHistoryPlaceholder(), ansiEscapeLen(), linenoiseCompletionCallback, linenoiseCompletions (+65 more)

### Community 9 - "Data Builtins"
Cohesion: 0.11
Nodes (77): char_pred, load_file(), tf_ctx, tf_ret, char_predicate(), find_mem(), index_in_bounds(), is_char_obj() (+69 more)

### Community 10 - "Meta Builtins and Hints"
Cohesion: 0.10
Nodes (74): repl_hints(), ascii_lower(), tf_ctx, tf_doc_entry, tf_obj, tf_ret, tf_type, tf_word (+66 more)

### Community 11 - "Core Numeric Builtins"
Cohesion: 0.11
Nodes (69): binary_math(), tf_ctx, tf_obj, tf_ret, checked_int_add(), checked_int_mul(), checked_int_sub(), compare_from_order() (+61 more)

### Community 12 - "Public API Layer"
Cohesion: 0.09
Nodes (67): tf_ctx_clear_error(), tf_ctx_set_error(), tf_obj_pool_enter(), tf_obj_pool_leave(), tf_package_word_name_valid(), api_errorf(), tf_obj, toy_resource_destructor (+59 more)

### Community 13 - "Builtin Generation Tools"
Cohesion: 0.05
Nodes (53): ref_fs, ref_path, ref_vscode, vscode-languageclient, cString(), fail(), fs, loadCorePackages() (+45 more)

### Community 14 - "Sequence Operations"
Cohesion: 0.14
Nodes (57): pair_items(), push_sequence_items_to_vector(), report_pair_error(), sequence_indexof(), sequence_len(), sequence_to_vector(), sort_string_bytes(), tf_concat() (+49 more)

### Community 15 - "Test Support Headers"
Cohesion: 0.06
Nodes (29): assert, CaptureBuffer, ctype, stb_leakcheck_free(), stb_leakcheck_malloc(), stb_leakcheck_realloc(), stblkck_internal_print(), printCapture() (+21 more)

### Community 16 - "REPL Runtime"
Cohesion: 0.09
Nodes (43): linenoise, repl_state, add_word_completion(), append_text(), linenoiseCompletions, tf_builtin_group, tf_ctx, tf_doc_entry (+35 more)

### Community 17 - "SQLite Extension"
Cohesion: 0.15
Nodes (43): toy_state, toy_status, toy_type, callable_type(), clear_update_handler(), copy_c_string(), destroy_database(), destroy_statement() (+35 more)

### Community 18 - "Toy Public Headers"
Cohesion: 0.10
Nodes (42): toy_state, toy_status, toy_type, toy_value, toy_call_value(), toy_clear_error(), toy_defer_call(), toy_deferred_count() (+34 more)

### Community 19 - "CLI Entry Point"
Cohesion: 0.07
Nodes (31): cli_config, dyld, signal, tf_ctx, core_directory_for_executable(), default_core_path(), directory_exists(), parse_args() (+23 more)

### Community 20 - "Debug Adapter Protocol"
Cohesion: 0.08
Nodes (32): event, launchArguments, messageWriter, request, response, setBreakpointsArguments, source, sourceBreakpoint (+24 more)

### Community 21 - "Nob Library API"
Cohesion: 0.14
Nodes (38): NOBDEF, nob_file_exists(), Nob_Log_Handler *nob_get_log_handler(void)(), nob_nanos_since_unspecified_epoch(), nob_path_name(), nob_set_log_handler(), Nob_String_View nob_sv_chop_by_delim(), Nob_String_View nob_sv_chop_left() (+30 more)

### Community 22 - "Toy Parser"
Cohesion: 0.19
Nodes (37): tf_source_span, tf_obj_set_span(), tf_source_file_release(), tf_ctx, tf_obj, tf_source_span, hex_value(), parser_advance() (+29 more)

### Community 23 - "Embedding API Tests"
Cohesion: 0.14
Nodes (35): stb_leakcheck_dumpmem(), main(), main(), tf_obj_new_call(), tf_obj_new_vector(), toy_eval(), toy_register_word(), toy_state_free() (+27 more)

### Community 24 - "Go Source Analysis"
Cohesion: 0.21
Nodes (30): LocalBinding, PackageImport, Privacy, SourceReference, SourceReferenceKind, tokenKind, go_pkg_unicode_utf16, go_pkg_unicode_utf8 (+22 more)

### Community 25 - "Debug Session Runner"
Cohesion: 0.13
Nodes (14): debugSession, machineEvent, machineFrame, machineValue, processOutput, Server, sessionConfig, go_pkg_os_exec (+6 more)

### Community 26 - "LSP Protocol Types"
Cohesion: 0.11
Nodes (33): definitionParams, didChangeTextDocumentParams, didCloseTextDocumentParams, didOpenTextDocumentParams, documentFormattingParams, documentSymbol, documentSymbolParams, formattingOptions (+25 more)

### Community 27 - "Tree-sitter Node Binding"
Cohesion: 0.06
Nodes (34): node-addon-api, node-gyp-build, prebuildify, tree-sitter, tree-sitter-cli, author, name, url (+26 more)

### Community 28 - "Bindgen C Fixtures"
Cohesion: 0.09
Nodes (17): test_bindgen_box, test_bindgen_child, allocate_box(), test_bindgen_box_destroy(), test_bindgen_box_error(), test_bindgen_box_label(), test_bindgen_box_new(), test_bindgen_box_open() (+9 more)

### Community 29 - "Benchmark Experiment Notes"
Cohesion: 0.09
Nodes (33): map vs fold and domain fast-path findings, Application Workload Drivers, Benchmark Workload Suite, Cross-language Benchmark Guide, Benchmarks Guide, Experiment: Compact recursion controllers, Experiment: Control-combinator snapshot ownership, Experiment: Multi-state graph traversal (+25 more)

### Community 30 - "Nob Command Runner"
Cohesion: 0.14
Nodes (31): nob_chain_begin_opt(), nob_chain_cmd_opt(), nob_chain_end_opt(), nob__cmd_append(), nob_cmd_render(), nob_cmd_run_async(), nob_cmd_run_async_and_reset(), nob_cmd_run_async_redirect() (+23 more)

### Community 31 - "Debug Inspector"
Cohesion: 0.12
Nodes (30): debug_print_locals(), parse_nonnegative_size(), tf_ctx, tf_debug_capture_info, tf_frame, tf_frame_kind, tf_word, debug_fill_word_info() (+22 more)

### Community 32 - "Embedding Examples"
Cohesion: 0.09
Nodes (25): toy_state, toy_value, fail(), main(), monotonic_ns(), toy_state, toy_status, hostLog() (+17 more)

### Community 33 - "IO Format Builtins"
Cohesion: 0.20
Nodes (28): FILE, tf_ctx, tf_obj, tf_obj_write_fn, tf_ret, consume_format_arguments(), ctx_output_obj_write(), ctx_write_value() (+20 more)

### Community 34 - "Go Formatter Config"
Cohesion: 0.15
Nodes (24): Config, DelimiterSpacing, IndentStyle, Options, sourceToken, SyntaxError, tokenRole, go_pkg_toy_tools_internal_parser (+16 more)

### Community 35 - "Go Source Lexer"
Cohesion: 0.22
Nodes (11): sourceLexer, containsLineBreak(), isASCIIAlpha(), isASCIIDigit(), isASCIIHex(), isASCIIWhitespace(), isStructuralByte(), isSymbolByte() (+3 more)

### Community 36 - "Go Formatter CLI"
Cohesion: 0.15
Nodes (25): go_pkg_unicode, asciiDigit(), asciiLetter(), buildCommands(), formatCommand(), isMSVCStyle(), libraryIsPath(), main() (+17 more)

### Community 37 - "Debug Protocol"
Cohesion: 0.20
Nodes (26): main(), FILE, tf_ctx, tf_debug_action, tf_debug_event, tf_obj, tf_ret, tf_source_span (+18 more)

### Community 38 - "LSP Resolution Cache"
Cohesion: 0.21
Nodes (9): definitionTarget, occurrenceKey, resolutionCache, wordOccurrence, Server, newResolutionCache(), packageDirectoryKey(), sameDefinition() (+1 more)

### Community 39 - "LSP Server Handlers"
Cohesion: 0.28
Nodes (11): io.Writer, response, Server, request, newResult(), decodeID(), Server, request (+3 more)

### Community 40 - "Debug Control"
Cohesion: 0.21
Nodes (22): tf_tdb_set_enabled(), any_breakpoint_matches(), append_breakpoint(), breakpoint_matches(), tf_debug_event, line_breakpoint_matches(), release_breakpoint(), tf_debug_control_add_line_breakpoint() (+14 more)

### Community 41 - "Nob Windows Shim"
Cohesion: 0.16
Nodes (24): DWORD, nob_copy_directory_recursively(), nob_copy_file(), nob_delete_file(), nob_dir_entry_close(), nob_dir_entry_next(), nob_dir_entry_open(), Nob_File_Type nob_get_file_type() (+16 more)

### Community 42 - "System Builtins"
Cohesion: 0.19
Nodes (18): direct, tf_ctx, tf_ret, shell_exit_status(), tf_argc(), tf_argv(), tf_cpu_time(), tf_env_q() (+10 more)

### Community 43 - "LSP Document Store"
Cohesion: 0.19
Nodes (9): time.Time, document, documentStore, fileURIFromPath(), ignoredWorkspaceDirectory(), isToySourcePath(), normalizedDocumentURI(), uniqueAbsolutePaths() (+1 more)

### Community 44 - "LSP Test Suite"
Cohesion: 0.29
Nodes (20): testResponse, decodeTestResponse(), TestDocumentFormattingReturnsRequestErrorForInvalidSyntax(), TestDocumentFormattingUsesProjectConfigOverLSPDefaults(), testFileURI(), TestInitializeAdvertisesDocumentFormatting(), TestCaptureRenamePreservesFetchPrefix(), TestDefinitionResponseFollowsImportSourceStrings() (+12 more)

### Community 45 - "Project Documentation"
Cohesion: 0.13
Nodes (21): Agent Guide (AGENTS.md), Repository Invariants, Experiment: Two inline capture bindings, Experiment: Bytecode sidecar (not retained), Experiment: Compact times execution, builtins.json Canonical Metadata, Opcode sidecar prototype for quotations, Source Build Guide (Nob) (+13 more)

### Community 46 - "Go SDK Tool"
Cohesion: 0.15
Nodes (17): go_pkg_errors, go_pkg_fmt, go_pkg_path_filepath, go_pkg_reflect, go_pkg_testing, go_pkg_toy_tools_internal_sdkroot, extractSDKRoot(), main() (+9 more)

### Community 47 - "Random and Locking"
Cohesion: 0.19
Nodes (18): fcntl, tf_lock_acquire(), tf_lock_release(), mix_seed(), system_random_bytes(), tf_random_init(), tf_random_int_range(), tf_random_seed() (+10 more)

### Community 48 - "Go CLI Formatter"
Cohesion: 0.16
Nodes (16): go_pkg_bytes, go_pkg_flag, go_pkg_io, go_pkg_toy_tools_internal_formatter, formatSource(), main(), run(), TestRunCheckAndWrite() (+8 more)

### Community 49 - "TextMate Grammar"
Cohesion: 0.10
Nodes (19): patterns, patterns, patterns, name, patterns, patterns, repository, comments (+11 more)

### Community 50 - "Go Formatter Tests"
Cohesion: 0.31
Nodes (18): testing.T, DefaultOptions(), Format(), readFixture(), TestDisabledFormatLeavesSourceUntouched(), TestDiscoverConfigParentToChildPrecedence(), TestFormatFixturesAndIdempotence(), TestFormatKeepsInlineAndMultilineVectorLayouts() (+10 more)

### Community 51 - "Cross-language Run Harness"
Cohesion: 0.18
Nodes (12): describe_run(), execute(), format_ms(), main(), parse_internal_time(), prepare_fixtures(), Runtime, runtimes() (+4 more)

### Community 52 - "Benchmark Comparison Library"
Cohesion: 0.22
Nodes (13): append_benchmark_path(), benchmark_path(), benchmark_platform(), collect_benchmarks(), compare_benchmarks(), Build_Config, Compile_Commands, File_Paths (+5 more)

### Community 53 - "Tree-sitter Config"
Cohesion: 0.12
Nodes (16): bindings, c, go, java, node, python, rust, swift (+8 more)

### Community 54 - "Go LSP Indexer"
Cohesion: 0.25
Nodes (14): positionMapper, github.com/tree-sitter/go-tree-sitter.Node, collectLocalBindings(), collectPackageDirectives(), collectTokensAndLocals(), collectTopLevelDefinitions(), decodeStringLiteral(), indexDefDefinition() (+6 more)

### Community 55 - "Measurement Scripts"
Cohesion: 0.17
Nodes (14): argparse, main(), Measure application phases separately from fixture construction and checks.…, sample(), main(), parse_phases(), Paired wall-time measurements of checked call-path diagnostic phases., Validate every case and checksum before accepting its elapsed time. (+6 more)

### Community 56 - "Benchmark Test Scripts"
Cohesion: 0.16
Nodes (14): Run with: python3 -m unittest discover -s benchmarks/cross-language -v, Run with: python3 -B -m unittest discover -s benchmarks -p 'test_*.py' -v, contextlib, dataclasses, core:json Reference, JSON Value Mapping, Shared Capability Vocabulary, importlib_util (+6 more)

### Community 57 - "Embedding Capture Tests"
Cohesion: 0.25
Nodes (13): capture_buffer, toy_state, toy_status, capture_clear(), capture_contains(), capture_equals(), host_defer(), host_defer_twice() (+5 more)

### Community 58 - "User Reference Docs"
Cohesion: 0.15
Nodes (16): Toy Data Model, Symbol vs Call Distinction, Editors and Formatting Guide, Installation Guide, Packages and Imports Reference, Toy REPL Guide, Release Workflow (CI), Multi-OS SDK Release Pipeline (+8 more)

### Community 59 - "Debug Printing"
Cohesion: 0.20
Nodes (16): tf_debug_action, tf_debug_event, tf_source_span, debug_add_breakpoint(), debug_print_backtrace(), debug_print_breakpoints(), debug_print_pause(), debug_print_span() (+8 more)

### Community 60 - "Native Plugin Tests"
Cohesion: 0.21
Nodes (13): TEST_DEPENDENCY_EXPORT, test_native_dependency_value(), toy_extension_api, TOY_EXTENSION_EXPORT, toy_state, toy_status, plugin_defer(), plugin_dependency_value() (+5 more)

### Community 61 - "Application Oracles"
Cohesion: 0.29
Nodes (12): advance(), analyze(), check_particles(), evaluate(), log_checksum(), log_text(), main(), quote() (+4 more)

### Community 62 - "Embedding Experiment Notes"
Cohesion: 0.18
Nodes (13): Experiment: Interpreter-state isolation, Experiment: Compact deferred-call storage, Single variable-sized deferred-call allocation, Deferred Call API (toy_defer_call), core:random Reference, State-owned PCG32 Stream, Embedding Toy in C, toy_state Public C Boundary (+5 more)

### Community 63 - "C Interop Docs"
Cohesion: 0.26
Nodes (13): Dynamic FFI (core:ffi), Generated Bindings, Handwritten C Extensions, Binding Manifest Reference, toy-bindgen Manifest Format, Using C Libraries, Basic C Extension Example, Generated Binding Examples (+5 more)

### Community 64 - "JavaScript Benchmark Workloads"
Cohesion: 0.18
Nodes (7): benchmarks, dispatch(), elapsed, fib(), inc(), result, started

### Community 65 - "Log Report JavaScript"
Cohesion: 0.18
Nodes (9): elapsed, fs, groups, analyze(), integer(), output, started, text (+1 more)

### Community 66 - "Native Library Loader"
Cohesion: 0.29
Nodes (11): dlfcn, tf_ctx, tf_ret, library_close(), library_entry(), library_error(), library_open(), remember_library() (+3 more)

### Community 67 - "Go LSP Analysis"
Cohesion: 0.18
Nodes (10): go_pkg_io_fs, go_pkg_net_url, go_pkg_runtime, go_pkg_sort, go_pkg_strings, go_pkg_time, go_pkg_toy_tools_internal_analysis, newDocumentStore() (+2 more)

### Community 68 - "Builtin Registry"
Cohesion: 0.26
Nodes (10): builtin_word_count(), tf_builtin_group, tf_ctx, register_builtin_group(), tf_builtin_groups(), tf_ctx_new(), tf_ctx_set_diagnostic(), tf_ctx_set_output() (+2 more)

### Community 69 - "LSP Index Tests"
Cohesion: 0.29
Nodes (11): DocumentSymbols(), IndexDocument(), TestBlockCommentDocumentation(), TestDocumentSymbols(), TestIndexPackageDirectives(), TestIndexUsesUTF16Columns(), TestLookupDefinition(), TestLookupHover() (+3 more)

### Community 70 - "Tree-sitter Grammar"
Cohesion: 0.21
Nodes (12): content, members, type, content, type, content, type, escape_sequence (+4 more)

### Community 71 - "Data Layout Experiments"
Cohesion: 0.18
Nodes (11): Experiment: Hybrid sort and hash-assisted unique, Experiment: Inline strings and direct result construction, Experiment: List-node slabs, Experiment: Immediate tagged integers, Collection Complexity Contracts, Hybrid sort / delayed-hash unique, Inline short-string storage in tf_obj, Bounded list-node slab allocator (+3 more)

### Community 73 - "FFI Fixtures"
Cohesion: 0.33
Nodes (10): FIXTURE_EXPORT, toy_ffi_add_i32(), toy_ffi_greeting(), toy_ffi_ignore_i32(), toy_ffi_large_u32(), toy_ffi_negative_i8(), toy_ffi_not(), toy_ffi_scale_f64() (+2 more)

### Community 74 - "LSP Builtin Docs"
Cohesion: 0.44
Nodes (8): builtinDoc, corePackageDoc, CorePackageName(), DefinitionHover(), docHover(), Hover, LookupCorePackageHover(), LookupHover()

### Community 75 - "Log Report Python"
Cohesion: 0.29
Nodes (9): main(), analyze(), checksum(), integer(), report(), Idiomatic port of examples/log-report: validated TSV -> grouped, sorted TSV., pathlib, re (+1 more)

### Community 76 - "Tree-sitter Go Bindings"
Cohesion: 0.22
Nodes (8): go_pkg_c, go_pkg_github_com_tree_sitter_go_tree_sitter, go_pkg_toy_tools_tree_sitter_toy_src, go_pkg_unsafe, github.com/tree-sitter/go-tree-sitter.Language, github.com/tree-sitter/go-tree-sitter.Tree, Parse(), Language()

### Community 77 - "Tree-sitter Grammar Spec"
Cohesion: 0.20
Nodes (9): conflicts, externals, extras, inline, name, precedences, reserved, $schema (+1 more)

### Community 78 - "Python Benchmark Workloads"
Cohesion: 0.25
Nodes (4): dispatch(), fib(), inc(), time

### Community 79 - "Capture Stack Experiments"
Cohesion: 0.22
Nodes (9): Experiment: Shared dynamic capture stack, Raw output: capture-stack GCC 15, Raw output: capture-stack GCC 16, Raw output: capture-stack JSON profile, Raw output: capture-stack log profile, Raw output: capture-stack particles profile, Raw output: capture-stack screening, Raw output: capture-stack self-comparison (+1 more)

### Community 80 - "Deferred Call Example"
Cohesion: 0.44
Nodes (8): toy_state, toy_status, toy_value, defer_message(), emit_twice(), main(), report_error(), value_is_callable()

### Community 81 - "Allocation Statistics"
Cohesion: 0.42
Nodes (8): allocation_site_calls(), allocation_site_hash(), allocation_site_precedes(), find_allocation_site(), record_allocation(), tf_alloc_stats_dump(), tf_alloc_kind, tf_alloc_site

### Community 82 - "Tree-sitter Grammar"
Cohesion: 0.22
Nodes (9): type, members, type, members, type, rules, block_comment, _expression (+1 more)

### Community 83 - "Lua Benchmark Workloads"
Cohesion: 0.29
Nodes (3): dispatch(), fib(), inc()

### Community 85 - "Call Path Experiments"
Cohesion: 0.25
Nodes (8): Experiment: Dispatch low-hanging candidates (discarded), Experiment: Shared call and conditional scheduling costs, Raw output: call-path conditional screen, Raw output: call-path GCC 15, Raw output: call-path GCC 16, Raw output: call-path prepared user applications, Four rejected call-path runtime prototypes, Dispatch change rejection on noisy timings

### Community 86 - "Nob String Builder"
Cohesion: 0.36
Nodes (8): nob_read_entire_file(), nob_sb_appendf(), nob_sb_pad_align(), nob_walk_dir_opt(), nob__walk_dir_opt_impl(), Nob_String_Builder, Nob_Walk_Dir_Opt, Nob_Walk_Func

### Community 87 - "Natural Sort"
Cohesion: 0.57
Nodes (8): natural_sort_kind, tf_obj, insertion_sort_items(), merge_sorted_runs(), natural_compare(), sort_vector_natural(), validate_natural_sort(), vector_contains_equal()

### Community 88 - "Core Package Docs"
Cohesion: 0.32
Nodes (7): tf_doc_entry, tf_core_package_doc_lookup(), tf_core_package_docs(), tf_doc_entries(), tf_doc_lookup(), tf_docs, tf_package_doc

### Community 89 - "Tree-sitter Toy Parser"
Cohesion: 0.25
Nodes (7): tree_sitter_toy(), ts_lex(), set_contains(), TS_PUBLIC, TSCharacterRange, TSLexer, TSStateId

### Community 90 - "Native Fast Path Experiments"
Cohesion: 0.29
Nodes (7): Experiment: Native execution fast paths, Raw output: native fast paths GCC 15, Raw output: native fast paths GCC 16, Raw output: native fast paths scalar, Raw output: native fast paths self-comparison, Raw output: native fast paths steps, Inline native argument checks and stack helpers

### Community 91 - "Tree-sitter Grammar"
Cohesion: 0.29
Nodes (7): value, content, type, number, _string_content, content, type

### Community 93 - "Nob Log Handlers"
Cohesion: 0.60
Nodes (5): va_list, nob_cancer_log_handler(), nob_default_log_handler(), nob_null_log_handler(), Nob_Log_Level

### Community 94 - "Nob Process Helpers"
Cohesion: 0.70
Nodes (5): nob_procs_append_with_flush(), nob_procs_flush(), nob_procs_wait(), nob_procs_wait_and_reset(), Nob_Procs

### Community 95 - "Builtin Word Lists"
Cohesion: 0.70
Nodes (3): builtinWords, controlWords, operatorWords

### Community 97 - "Tree-sitter Grammar"
Cohesion: 0.67
Nodes (3): members, type, block

### Community 98 - "Tree-sitter Grammar"
Cohesion: 0.67
Nodes (3): members, type, boolean

### Community 99 - "Tree-sitter Grammar"
Cohesion: 0.67
Nodes (3): members, type, builtin_word

### Community 100 - "Tree-sitter Grammar"
Cohesion: 0.67
Nodes (3): members, type, _comment

### Community 101 - "Tree-sitter Grammar"
Cohesion: 0.67
Nodes (3): members, type, control_word

### Community 102 - "Tree-sitter Grammar"
Cohesion: 0.67
Nodes (3): members, type, list_literal

### Community 103 - "Tree-sitter Grammar"
Cohesion: 0.67
Nodes (3): members, type, map_literal

### Community 104 - "Tree-sitter Grammar"
Cohesion: 0.67
Nodes (3): members, type, _non_capture_expression

### Community 105 - "Tree-sitter Grammar"
Cohesion: 0.67
Nodes (3): members, type, operator

### Community 106 - "Tree-sitter Grammar"
Cohesion: 0.67
Nodes (3): set_literal, members, type

### Community 107 - "Tree-sitter Grammar"
Cohesion: 0.67
Nodes (3): string, members, type

### Community 108 - "Tree-sitter Grammar"
Cohesion: 0.67
Nodes (3): var_fetch, members, type

### Community 109 - "Tree-sitter Grammar"
Cohesion: 0.67
Nodes (3): var_list, members, type

### Community 110 - "Tree-sitter Grammar"
Cohesion: 0.67
Nodes (3): word, type, value

## Knowledge Gaps
- **216 isolated node(s):** `benchmarks`, `started`, `result`, `elapsed`, `fs` (+211 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 476 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Runtime Internals` connect `Project Documentation` to `Dispatch Performance Experiments`, `Packages and Word Lookup`, `Builtin Registry`, `Data Layout Experiments`, `Toy Public Headers`, `Native Fast Path Experiments`, `Debug Inspector`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `tf_obj_release()` connect `Meta Builtins and Hints` to `Control Word Builtins`, `IO Format Builtins`, `Dispatch Performance Experiments`, `Packages and Word Lookup`, `Object Runtime Core`, `Debug Protocol`, `Data Builtins`, `System Builtins`, `Core Numeric Builtins`, `Public API Layer`, `Sequence Operations`, `REPL Runtime`, `CLI Entry Point`, `Toy Parser`, `Embedding API Tests`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `Toy README` connect `User Reference Docs` to `Project Documentation`, `Benchmark Test Scripts`, `Benchmark Experiment Notes`, `Embedding Experiment Notes`, `C Interop Docs`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Are the 200 inferred relationships involving `tf_obj_release()` (e.g. with `write_source_value()` and `load_file()`) actually correct?**
  _`tf_obj_release()` has 200 INFERRED edges - model-reasoned connections that need verification._
- **Are the 159 inferred relationships involving `tf_stack_push()` (e.g. with `app2_step()` and `bi_step()`) actually correct?**
  _`tf_stack_push()` has 159 INFERRED edges - model-reasoned connections that need verification._
- **Are the 136 inferred relationships involving `tf_stack_pop()` (e.g. with `app2_step()` and `bi_step()`) actually correct?**
  _`tf_stack_pop()` has 136 INFERRED edges - model-reasoned connections that need verification._
- **Are the 117 inferred relationships involving `tf_obj_typeof()` (e.g. with `write_source_value()` and `cond_step()`) actually correct?**
  _`tf_obj_typeof()` has 117 INFERRED edges - model-reasoned connections that need verification._