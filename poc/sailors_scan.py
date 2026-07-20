"""
sailors_scan.py

A small proof-of-concept scanner for the SAILORS framework.

This is intentionally simple: it reads a Python file line by line and
flags lines that match patterns associated with each SAILORS check. It
is a keyword/pattern scanner, not a full static-analysis tool (no AST
parsing, no data-flow tracking) -- it is meant to demonstrate that
SAILORS' seven checks can produce real, concrete findings against real
code, not just serve as a talking-point checklist.

Usage:
    python sailors_scan.py test_pto_assistant.py
"""

import sys


def scan_file(filepath):
    findings = []

    with open(filepath, "r") as f:
        lines = f.readlines()

    has_log_call = False

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        # R -- Record every action.
        # Look for any logging call anywhere in the file.
        if "log(" in stripped or "logging." in stripped or "print(\"LOG" in stripped:
            has_log_call = True

        # S -- Sanitize inputs.
        # Flag raw input() calls with no nearby validation/stripping.
        if "input(" in stripped and ".strip()" not in stripped and "len(" not in stripped:
            findings.append(f"[S] Line {i}: input not sanitized -- {stripped}")

        # A -- Access controls at retrieval.
        # Flag queries that look like they pull everyone's data, not one
        # user's -- e.g. a SELECT with no WHERE clause scoping by user.
        if "select" in stripped.lower() and "where" not in stripped.lower():
            findings.append(f"[A] Line {i}: retrieval has no per-user scoping -- {stripped}")

        # L -- Least privilege for tools.
        # Flag overly broad permission grants.
        if "admin" in stripped.lower() or "all_permissions" in stripped.lower():
            findings.append(f"[L] Line {i}: overly broad permission grant -- {stripped}")

        # O -- Override gate for humans (action + scope).
        # Flag consequential-sounding actions with no nearby confirm/approval check.
        # Skip function definitions themselves -- only flag call sites.
        if not stripped.startswith("def "):
            action_keywords = ["file_request(", "approve_transaction(", "submit(", "approve_"]
            gate_keywords = ["confirm(", "manager_approval", "requires_approval"]
            if any(k in stripped for k in action_keywords):
                nearby = "".join(lines[max(0, i - 3):i + 2])
                if not any(g in nearby for g in gate_keywords):
                    findings.append(f"[O] Line {i}: consequential action with no nearby override gate -- {stripped}")

    # R -- Record every action (file-level check, not line-level).
    if not has_log_call:
        findings.append("[R] No logging/audit calls found anywhere in this file")

    return findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python sailors_scan.py <path_to_python_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    findings = scan_file(filepath)

    print(f"\nSAILORS scan results for: {filepath}")
    print("-" * 60)

    if not findings:
        print("No findings -- no patterns matched.")
    else:
        for finding in findings:
            print(finding)

    print("-" * 60)
    print(f"{len(findings)} finding(s).\n")
    print("Note: this is a lightweight keyword/pattern scanner, not full")
    print("static analysis. Findings are a starting point for manual")
    print("SAILORS review, not a replacement for it.")


if __name__ == "__main__":
    main()
