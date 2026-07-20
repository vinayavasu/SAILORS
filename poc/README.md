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

```bash
python sailors_scan.py test_pto_assistant.py
```

`test_pto_assistant.py` is a small, deliberately flawed example --
several SAILORS checks are intentionally violated in it so the scanner
has real findings to catch. Expect output like:

```
[A] Line 10: retrieval has no per-user scoping -- ...
[S] Line 14: input not sanitized -- ...
[O] Line 17: consequential action with no nearby override gate -- ...
[L] Line 23: overly broad permission grant -- ...
[R] No logging/audit calls found anywhere in this file
```

## Checks currently covered

| Letter | Covered in this PoC? | How |
|---|---|---|
| S -- Sanitize inputs | Yes | Flags `input()` calls with no nearby validation |
| A -- Access controls at retrieval | Yes | Flags queries with no per-user scoping |
| I -- Inspect and filter outputs | Not yet | |
| L -- Least privilege for tools | Yes | Flags overly broad permission grants |
| O -- Override gate for humans | Yes | Flags consequential actions with no nearby confirm/approval |
| R -- Record every action | Yes | Flags files with no logging calls at all |
| S -- System prompt hardening | Not yet | |

I and the second S are harder to catch with pattern matching alone (they
depend on context an AST or LLM-based pass would handle better) -- left
out of this first pass rather than faked with a shallow, unreliable check.

## Try it on your own code

```bash
python sailors_scan.py path/to/your_file.py
```

Run it against a real AI capability you're working on and see what it
finds. If you get a false positive, false negative, or want to extend
coverage to I or the second S, that's exactly the kind of contribution
this PoC needs -- open an issue or PR.
