# SAILORS

**A practitioner-level threat modeling framework for individual AI capabilities.**

STRIDE was built for traditional software systems. MAESTRO addresses agentic AI systems at the architecture level. Neither answers the question a team actually asks the moment they say "we're adding this AI feature": **what do we check before we ship it?**

SAILORS fills that gap.

## Where SAILORS Fits

| Framework | Scope | Question it answers |
|---|---|---|
| STRIDE | Traditional systems | What can go wrong with this system's data flows? |
| MAESTRO | Agentic AI architectures | What can go wrong across this multi-agent system? |
| **SAILORS** | **Individual AI capabilities** | **What do we check before this specific AI feature ships, and again at every significant change?** |

SAILORS is designed to be used at the feature level: a single RAG pipeline, a single tool-calling capability, a single LLM-backed endpoint, not the whole system or the whole agent architecture. It's meant to be fast enough to run in a design review, not just a compliance exercise.

## The Framework

| Letter | Principle | What it checks |
|---|---|---|
| **S** | Sanitize all inputs | Are user/tool inputs validated, encoded, and bounded before reaching the model? |
| **A** | Access controls at retrieval | Does retrieval (RAG, tool calls, memory) respect the requesting user's actual permissions? If retrieval is itself another agent's output, this becomes a MAESTRO question. Cross-agent trust isn't a single-capability fix. |
| **I** | Inspect and filter outputs | Is model output checked before it's rendered, executed, or passed downstream? |
| **L** | Least privilege for tools | Does the capability hold only the permissions it needs, nothing more? Includes resource-usage scope. Token exhaustion and unbounded tool calls are permission problems, not input problems. |
| **O** | Override gate for humans (action + scope) | Is there a human checkpoint before (1) a consequential action fires, and (2) any expansion in the capability's scope or permissions during a session? |
| **R** | Record every action | Is there an audit trail sufficient to reconstruct what happened and why? If the agent writes its own log, the log is only as trustworthy as the agent. Route logs through a channel the capability can't modify, where possible. |
| **S** | System prompt hardening | Is the system prompt resistant to injection, leakage, and override attempts? |

## Review Template

SAILORS is not just a checklist. It is a structured review process. The [review template](templates/sailors-review-template.md) gives teams a fillable document for a 30-minute design review:

- Capability information (model, data sources, tools, outputs)
- All 7 checks with status (PASS / FAIL / PARTIAL / N/A), evidence, findings, severity, and release blocker flag
- Summary with top risks, required fixes, accepted risks, and final decision
- Next review trigger section

Print it, bring it to a design review, fill it out. That is how SAILORS is meant to be used.

## AIBOM Trigger

SAILORS reviews do not happen in a vacuum. They are triggered by changes to your AI Bill of Materials (AIBOM).

The [AIBOM trigger document](docs/aibom-trigger.md) defines:

- Minimal AIBOM fields for one AI capability
- 10 trigger events that should start a SAILORS review
- A trigger matrix that tells you which checks to re-run for each type of change (not all 7 every time)
- Three workflow options: manual, pull request trigger, and CI/CD gate

AIBOM tells you what AI capabilities exist and what changed. SAILORS tells you what to review before that capability ships.

## How to Use It

1. Identify the AI capability being shipped: a feature, not a full system.
2. Open the [review template](templates/sailors-review-template.md).
3. Walk each SAILORS letter as a checklist item against that capability.
4. Flag gaps as findings, prioritize by exploitability and blast radius.
5. Document the decision: ship, ship with fixes, or block.
6. Re-run at each significant capability change (use the AIBOM trigger matrix to know which checks to re-run).

A worked example is included in `/examples`.

## SAILORS-Verify: PoC Scanner

SAILORS-Verify is a lightweight proof-of-concept scanner that runs SAILORS' seven checks against real Python code.

- It covers **5 of 7 checks**:
  - S — Sanitize all inputs
  - A — Access controls at retrieval
  - L — Least privilege for tools
  - O — Override gate for humans
  - R — Record every action
- It uses pattern matching.
- It does not yet cover:
  - I — Inspect and filter outputs
  - System prompt hardening
  - Three refined sub-checks that require cross-file context
- It is explicitly described as **not full static analysis**.
- It is intended as a starting point for a manual review, not a replacement for one.

The scanner, a test file, and example output are in `/poc`.

## Mapping to Existing Standards

SAILORS is cross-referenced against:

- OWASP Top 10 for LLM Applications (2026)
- OWASP Top 10 for Agentic Applications (2026)
- MITRE ATLAS tactics, where applicable at the capability level

The full mapping table is in [mapping.md](mapping.md). A coverage matrix showing what SAILORS covers directly, partially, and what companion controls fill the gaps is in [docs/owasp-coverage-matrix.md](docs/owasp-coverage-matrix.md).

SAILORS provides direct or partial design-time coverage for most capability-level OWASP LLM and Agentic risks. For architecture-level and runtime risks (supply chain, data poisoning, unbounded consumption, inter-agent communication), SAILORS defines companion controls rather than extending the 7-check scope.

## What Comes After SAILORS

SAILORS covers the design review: what to check before a capability ships. Two frameworks go deeper once the capability is built and deployed:

### RAISE

- Full name: **Responsible AI Software Engineering**
- Description: Steve Wilson's maturity model for how an agent is engineered, secured, tested, and operated.
- It assesses six categories:
  1. Zero Trust
  2. Knowledge Base
  3. Domain Limits
  4. Monitoring
  5. Supply Chain
  6. AI Red Team

### Praxen

- Description: An open-source agent behavior verifier.
- It reads an agent's code and deployment state.
- It checks the agent against a declared policy called **Worker Remit**.
- It produces a scored posture report with `file:line` evidence.

The README distinguishes the frameworks as follows:

- SAILORS asks the questions at design time.
- RAISE assesses maturity across the agent's engineering.
- Praxen verifies that the controls are actually implemented after the code exists.

A worked comparison of SAILORS and Praxen/RAISE against a deliberately broken demo agent named **FinBot** is in `/praxen-comparison`. It includes a full FinBot analysis report.

## Status

SAILORS is an early-stage, open framework with:

- 7-check review checklist
- Fillable review template for 30-minute design reviews
- AIBOM trigger model connecting capability changes to reviews
- SAILORS-Verify PoC scanner (5 of 7 checks)
- Mapping to OWASP LLM Top 10 and MITRE ATLAS
- Worked examples and Praxen comparison

Current status: v1.0. Seeking practitioner feedback from teams shipping AI capabilities. See the [review template](templates/sailors-review-template.md) to try it on one of your features.

## Changelog

### v1.0 (August 2026)

- Added review template (`templates/sailors-review-template.md`): Fillable document for 30-minute design reviews with status, evidence, findings, severity, and release blocker for each check.
- Added AIBOM trigger model (`docs/aibom-trigger.md`): Defines how AIBOM changes trigger SAILORS reviews, including trigger matrix for selective check re-runs.
- Updated README with review template and AIBOM trigger sections.
- Updated "How to Use It" section to reference the review template.

### August 2026

- Updated OWASP LLM Top 10 mapping to 2026 edition (released August 4, 2026).
- Added OWASP Agentic Top 10 (2026) mapping.
- Added coverage matrix (`docs/owasp-coverage-matrix.md`) showing direct, partial, and companion control coverage.
- Key change: Excessive Agency moved from #6 to #3; System Prompt Leakage renamed to Hidden Context Exposure; Improper Output Handling dropped from #5 to #10.
  
### July 2026

Two checks were revised after practitioner review from **Harshad Sadashiv Kadam**:

- **O** now covers two conditions instead of one:
  1. Gating the action itself.
  2. Separately gating any mid-session growth in the capability's scope or permissions.
- **A** now includes an explicit hand-off rule:
  - When retrieval is another agent's output rather than a static lookup, defer to MAESTRO instead of stretching A to cover it.

### Three refinements following review from **Shivam Dhar**

- **L** now explicitly covers resource-usage scope:
  - Token exhaustion and unbounded tool calls are permission problems, not input problems.
- **R** now includes a log-trust note for agent-written audit trails.
- The framing question now reflects continuous re-running, not just pre-ship review.

## Roadmap

- **SAILORS-Verify** (`/poc`) is live.
  - It covers 5 of 7 checks: S, A, L, O, and R.
  - It is a pattern-matching scanner.
  - The next step is AST-based analysis for cross-file checks:
    - A's MAESTRO hand-off
    - O's scope-expansion gate
    - R's log-trust note
  - Additional planned coverage includes:
    - I
    - System prompt hardening
- **CI integration**
  - The project is exploring how to run SAILORS-Verify as a pre-merge gate rather than only as a standalone script.
- **AIBOM pairing**
  - The AIBOM trigger model is now defined in `/docs/aibom-trigger.md`.
  - The next step is to automate the trigger: detect AIBOM changes in a PR and suggest which SAILORS checks to re-run.

## Author

- **Name:** Vinaya Vasudevan
- **Role:** AI Security Engineer
- **Credentials:** CAISP
- **Portfolio:** SANS AIS247 Portfolio
- **Website:** `vinayavasu.github.io`
- **Writing:** [Prompt to Patch](https://prompt-to-patch-vinaya.hashnode.dev/)
- **LinkedIn:** [vinayavasudevan](https://www.linkedin.com/in/vinaya-vasudevan/)

## Contributing

- Issues and pull requests are welcome.
- For people using SAILORS on a real capability review, an example write-up, including an anonymized one, is described as one of the most useful contributions at this stage.

## License

- MIT
