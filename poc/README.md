# SAILORS-Verify (proof of concept)

A small proof-of-concept scanner that runs SAILORS' seven checks against
real Python code, instead of just describing what they'd catch.

## What this is

`sailors_scan.py` reads a Python file line by line and flags patterns
associated with each SAILORS check: unsanitized input, retrieval with no
per-user scoping, overly broad permission grants, consequential actions
with no nearby override gate, and missing audit logging.

**What this is not:** full static analysis. There's no AST parsing, no
data-flow tracking, no cross-file analysis -- it's a lightweight
keyword/pattern scanner. Findings are a starting point for a manual
SAILORS review, not a replacement for one. That's an intentional
scoping choice for this first pass, not a hidden limitation.

## Try it

```
python sailors_scan.py test_pto_assistant.py
```

`test_pto_assistant.py` is a small, deliberately flawed example --
several SAILORS checks are intentionally violated in it so the scanner
has real findings to catch.

## Example output

Running it against the included `test_pto_assistant.py`:

```
SAILORS scan results for: test_pto_assistant.py
------------------------------------------------------------
[A] Line 10: retrieval has no per-user scoping -- return query_database("SELECT * FROM employees")
[S] Line 14: input not sanitized -- raw_days = input("How many days off do you want? ")  # S: no sanitization
[O] Line 17: consequential action with no nearby override gate -- file_request(employee_id, raw_days)  # O: fires immediately, no manager gate
[L] Line 23: overly broad permission grant -- user.permissions = "admin"
[L] Line 24: overly broad permission grant -- user.all_permissions = True
[O] Line 29: consequential action with no nearby override gate -- approve_transaction(amount)
[L] Line 34: unbounded loop with no visible call limit -- while True:
[R] No logging/audit calls found anywhere in this file
------------------------------------------------------------
8 finding(s).

Note: this is a lightweight keyword/pattern scanner, not full
static analysis. Findings are a starting point for manual
SAILORS review, not a replacement for it.
```

Eight findings, one for each intentional flaw baked into the test file --
no false positives, no crashes.

## What's new here vs. the SAILORS framework definition

The main README's L check now also covers resource-usage scope (token
exhaustion, unbounded tool calls) -- following feedback from a
practitioner review. This scanner now catches one concrete pattern of
that: an unbounded loop (`while True` with no visible break/limit)
sitting near a downstream call.

**Worth being upfront about what this PoC does *not* yet catch,** even
though the framework definition now covers it:

- **A's MAESTRO hand-off** (retrieval from another agent vs. a static
  lookup) -- not detectable by reading one file's text. Knowing whether
  a function call is "another agent's output" requires understanding
  the broader system, not just this file.
- **O's scope-expansion gate** (a capability quietly gaining new tools
  or permissions across a session) -- requires comparing state over
  time, not something visible in a single static read of one file.
- **R's log-trust note** (whether a log entry was written by the agent
  itself vs. an independent system) -- requires knowing *who* wrote a
  given log call, not just whether one exists.

Same honest category as I and the second S below: these are context-
dependent checks that pattern matching structurally can't do well.
Faking a shallow check for them would be worse than leaving them out.

## Checks currently covered

| Letter | Covered in this PoC? | How |
|---|---|---|
| S -- Sanitize inputs | Yes | Flags `input()` calls with no nearby validation |
| A -- Access controls at retrieval | Yes | Flags queries with no per-user scoping |
| I -- Inspect and filter outputs | Not yet | |
| L -- Least privilege for tools | Yes (partial) | Flags overly broad permission grants, and unbounded loops with no visible call limit |
| O -- Override gate for humans | Yes | Flags consequential actions with no nearby confirm/approval |
| R -- Record every action | Yes | Flags files with no logging calls at all |
| S -- System prompt hardening | Not yet | |

I and the second S are harder to catch with pattern matching alone (they
depend on context an AST or LLM-based pass would handle better) -- left
out of this first pass rather than faked with a shallow, unreliable check.

## Try it on your own code

```
python sailors_scan.py path/to/your_file.py
```

Run it against a real AI capability you're working on and see what it
finds. If you get a false positive, false negative, or want to extend
coverage to I or the second S, that's exactly the kind of contribution
this PoC needs -- open an issue or PR.
