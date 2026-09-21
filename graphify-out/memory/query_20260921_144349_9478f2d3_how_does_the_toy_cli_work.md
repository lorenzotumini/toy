---
type: "query"
date: "2026-09-21T14:43:49.709264+00:00"
question: "how does the toy cli work?"
contributor: "graphify"
outcome: "useful"
source_nodes: ["main()", "tf_run_repl()", "tf_run_file()", "tf_run_string()", "run_source()"]
---

# Q: how does the toy cli work?

## Answer

Expanded from original query via vocab: [cli, repl, main, command, argument, flag, input, script, run, interactive, launch]. Traversal of main() (src/cli/main.c:64), tf_run_repl (src/cli/tf_repl.c:803), tf_run_file (L91), tf_run_string (L961), run_source (L926). The CLI parses args (parse_args, main.c:175), creates a tf_ctx, installs the optional debug protocol, then dispatches: -e style strings via tf_run_string, files via tf_run_file (sets import base to file's parent dir), packages via tf_package_run_main, and falls back to the interactive REPL (tf_run_repl) which reads lines with linenoise (read_repl_line), interprets REPL-only commands via repl_command_for_source, otherwise parses (tf_parse_source) and executes (tf_vm_exec) via run_source, printing results with tf_obj_print. Teardown: tf_debug_protocol_finish/free, tf_ctx_free, leak/alloc stats dumps.

## Outcome

- Signal: useful

## Source Nodes

- main()
- tf_run_repl()
- tf_run_file()
- tf_run_string()
- run_source()