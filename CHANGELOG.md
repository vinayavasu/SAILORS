# Changelog

All notable changes to SAILORS are recorded here.

## v1.1 (August 2026)

- Repositioned SAILORS from "threat modeling framework" to "security controls framework" based on expert review from the OWASP AI security community.
- Added "What SAILORS is (and is not)" section to clarify positioning.
- Added threat modeling as a prerequisite step in "How to use it."
- Added "Known limitations" section documenting the cloud AI service configuration gap.

## v1.0 (August 2026)

- Added review template (`templates/sailors-review-template.md`): fillable document for 30-minute design reviews with status, evidence, findings, severity, and release blocker per check.
- Added AIBOM trigger model (`docs/aibom-trigger.md`): defines how AIBOM changes trigger SAILORS reviews, including a trigger matrix for selective check re-runs.
- Updated README with review template and AIBOM trigger sections.
- Updated "How to use it" section to reference the review template.

## August 2026 (standards refresh)

- Updated OWASP LLM Top 10 mapping to the 2026 edition (released August 4, 2026).
- Added OWASP Agentic Top 10 (2026) mapping.
- Added coverage matrix (`docs/owasp-coverage-matrix.md`) showing direct, partial, and companion control coverage.
- Key changes in the 2026 taxonomy: Excessive Agency moved from #6 to #3. System Prompt Leakage renamed to Hidden Context Exposure. Improper Output Handling dropped from #5 to #10.

## July 2026 (practitioner feedback)

Two checks were revised after practitioner review from **Harshad Sadashiv Kadam**:

- **O** now covers two conditions instead of one:
  1. Gating the action itself.
  2. Separately gating any mid-session growth in the capability's scope or permissions.
- **A** now includes an explicit hand-off rule: when retrieval is another agent's output rather than a static lookup, defer to MAESTRO instead of stretching A to cover it.

Three refinements following review from **Shivam Dhar**:

- **L** now explicitly covers resource-usage scope. Token exhaustion and unbounded tool calls are permission problems, not input problems.
- **R** now includes a log-trust note for agent-written audit trails.
- The framing question now reflects continuous re-running, not just pre-ship review.

---

## Roadmap

- **SAILORS-Verify** (`/poc`) is live.
  - Covers 5 of 7 checks: S, A, L, O, R.
  - Pattern-matching scanner.
  - Next step: AST-based analysis for the cross-file checks. See [issue #3](https://github.com/vinayavasu/SAILORS/issues/3).
  - Additional planned coverage: I and system prompt hardening.
- **CI integration.** Exploring how to run SAILORS-Verify as a pre-merge gate rather than a standalone script.
- **AIBOM pairing.** The trigger model is now defined in `/docs/aibom-trigger.md`. Next step: automate the trigger detection, and pilot the matrix with real teams. See [issue #2](https://github.com/vinayavasu/SAILORS/issues/2).
