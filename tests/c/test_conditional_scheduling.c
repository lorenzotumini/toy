#include "tf_exec.h"
#include "tf_builtins.h"

#include <stdio.h>
#include <string.h>

#ifdef STB_LEAKCHECK
#include "tf_alloc.h"
#endif

#define CHECK(condition, message)                                            \
    do {                                                                     \
        if (!(condition)) {                                                  \
            fprintf(stderr, "conditional scheduling check failed: %s\n",    \
                    message);                                                \
            return 1;                                                        \
        }                                                                    \
    } while (0)

static toy_value *deferred_increment;
static int destroyed;
static size_t probes;

static void discard(void *userdata, const char *text, size_t length) {
    (void)userdata;
    (void)text;
    (void)length;
}

static toy_status branch_probe(toy_state *state) {
    probes++;
    size_t depth = state->call_stack_len;
    if (destroyed || depth < 3 ||
        state->call_stack[depth - 1].kind != TF_FRAME_PROGRAM ||
        state->call_stack[depth - 2].kind != TF_FRAME_NATIVE) {
        return toy_fail(state, "branch must retain its ordinary frames and inputs");
    }
    return TOY_OK;
}

static tf_debug_action step(tf_ctx *ctx, const tf_debug_event *event, void *data) {
    (void)ctx;
    (void)event;
    (*(size_t *)data)++;
    return TF_DEBUG_STEP;
}

static toy_status queue_then_if(toy_state *state) {
    toy_status status = toy_defer_call(state, deferred_increment, 0);
    return status == TOY_OK ? tf_if(state) : status;
}

static toy_status interrupt_then_if(toy_state *state) {
    toy_interrupt(state);
    return tf_if(state);
}

static void destroy_resource(void *resource, void *userdata) {
    (void)resource;
    (void)userdata;
    destroyed++;
}

static bool single_int(toy_state *state, int64_t expected) {
    int64_t value;
    return toy_stack_size(state) == 1 && toy_get_int(state, 0, &value) &&
           value == expected && toy_pop(state, 1);
}

int main(void) {
    toy_state_config config = {.diagnostic = discard};
    toy_state *state = toy_state_new(&config);
    CHECK(state, "create context");
    CHECK(toy_register_word(state, "branch-probe", branch_probe) == TOY_OK &&
              toy_register_word(state, "queue-then-if", queue_then_if) == TOY_OK &&
              toy_register_word(state, "interrupt-then-if", interrupt_then_if) == TOY_OK,
          "register test callbacks");

    size_t events = 0;
#ifdef TF_OBSERVE
    uint64_t continuation_steps[2], program_frames[2], native_frames[2];
#endif
    for (size_t debug = 0; debug < 2; debug++) {
        tf_debug_set_hook(state, debug ? step : NULL, &events);
#ifdef TF_OBSERVE
        tf_runtime_metrics before = state->metrics;
#endif
        CHECK(toy_eval(state, "<conditional-frames>",
                       "true [ branch-probe ] if "
                       "[ true ] [ branch-probe ] [] ifelse") == TOY_OK,
              "boolean and predicate branches preserve frames");
#ifdef TF_OBSERVE
        continuation_steps[debug] = state->metrics.native_continuation_steps -
                                    before.native_continuation_steps;
        program_frames[debug] = state->metrics.program_frames - before.program_frames;
        native_frames[debug] = state->metrics.native_frames - before.native_frames;
#endif
        CHECK(toy_eval(state, "<conditional-scopes>",
                       "10 | x | true [ 20 | x | $x ] if "
                       "[ 30 | x | true ] [ $x + ] if $x +") == TOY_OK &&
                  single_int(state, 40),
              "branch and predicate captures shadow locally then disappear");
        CHECK(state->captures_len == 0 && state->call_stack_len == 0,
              "completed conditionals release scopes and frames");
        CHECK(toy_eval(state, "<predicate-snapshot>",
                       "1 2 [ empty 99 true ] [ + ] if") == TOY_OK &&
                  single_int(state, 3), "predicate stack effects remain sandboxed");
        CHECK(toy_eval(state, "<predicate-scratch>",
                       "0 64 range [ [ empty true ] [] if ] infra len") == TOY_OK &&
                  single_int(state, 64), "large predicate snapshot storage unwinds in order");
        CHECK(toy_eval(state, "<conditional-error>",
                       "5 [ [ empty true ] [ 9 missing-word ] if ] "
                       "[ drop 1 + ] try") == TOY_OK && single_int(state, 6),
              "body errors retain enclosing try recovery");
        CHECK(toy_eval(state, "<predicate-error>",
                       "5 [ [ 99 ] [] if ] [ drop 1 + ] try") == TOY_OK &&
                  single_int(state, 6), "nonboolean predicate fails through ordinary recovery");
    }
    CHECK(probes == 4 && events > 0, "both paths execute and debugger receives instructions");
#ifdef TF_OBSERVE
    /* Scheduling may skip internal steps without an observer, but executing
     * the same branches must preserve the visible frame model. */
    CHECK(continuation_steps[0] <= continuation_steps[1] &&
              program_frames[0] == program_frames[1] && native_frames[0] == native_frames[1],
          "observed execution preserves program and native frames");
#endif
    tf_debug_set_hook(state, NULL, NULL);

    CHECK(toy_eval(state, "<deferred-handler>", "[ 1 + ]") == TOY_OK,
          "create deferred handler");
    deferred_increment = toy_value_retain(state, 0);
    CHECK(deferred_increment && toy_pop(state, 1), "retain handler");
    CHECK(toy_eval(state, "<deferred-before-predicate>",
                   "41 [ 42 == ] [ 1 + ] queue-then-if") == TOY_OK &&
              single_int(state, 43),
          "queued handler runs before predicate snapshots ambient stack");
    toy_value_release(deferred_increment);
    deferred_increment = NULL;

    CHECK(toy_eval(state, "<interrupt-before-predicate>",
                   "7 [ empty true ] [ branch-probe ] interrupt-then-if") == TOY_INTERRUPTED &&
              single_int(state, 7) && state->call_stack_len == 0 && state->scratch.depth == 0,
          "pending interruption runs no predicate and cleans its continuation");

    CHECK(toy_eval(state, "<symbol-fallback>",
                   "true [] ifelse") == TOY_ERROR,
          "argument validation still reports malformed conditionals");
    CHECK(toy_pop(state, toy_stack_size(state)), "clear failed stack");
    CHECK(toy_eval(state, "<symbol-calls>",
                   "'yes [ true ] def 'inc [ 1 + ] def "
                   "41 'yes 'inc if false 'inc [] ifelse") == TOY_OK && single_int(state, 42),
          "symbols retain the general iterative dispatch path");
    CHECK(toy_eval(state, "<symbol-recursion>",
                   "true [] 20000 [ true 'if ] times if") == TOY_OK &&
              toy_stack_size(state) == 0, "symbol-selected combinators stay iterative");

    CHECK(toy_eval(state, "<unchosen-resource>", "true [ branch-probe ]") == TOY_OK &&
              toy_push_resource(state, "conditional-test", &destroyed, destroy_resource, NULL) == TOY_OK,
          "prepare resource in unchosen quotation");
    tf_obj *unchosen = tf_obj_new_vector();
    tf_vector_push(unchosen, tf_stack_pop(state));
    tf_stack_push(state, unchosen);
    CHECK(toy_eval(state, "<resource-lifetime>", "ifelse") == TOY_OK && destroyed == 1,
          "unchosen input survives branch execution and releases exactly once");
    CHECK(toy_stack_size(state) == 0 && state->captures_len == 0 &&
              state->call_stack_len == 0 && state->scratch.depth == 0,
          "all execution storage is inactive at completion");
    toy_state_free(state);
#ifdef STB_LEAKCHECK
    stb_leakcheck_dumpmem();
#endif
    return 0;
}
