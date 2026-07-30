# SAILORS

**A practitioner-level threat modeling framework for individual AI capabilities.**

STRIDE was built for traditional software systems. MAESTRO addresses agentic AI systems at the architecture level. Neither answers the question a team actually asks the moment they say *"we're adding this AI feature"*: **what do we check before we ship it?**

SAILORS fills that gap.

---

## Where SAILORS Fits

| Framework | Scope | Question it answers |
|---|---|---|
| STRIDE | Traditional systems | What can go wrong with this system's data flows? |
| MAESTRO | Agentic AI architectures | What can go wrong across this multi-agent system? |
| **SAILORS** | **Individual AI capabilities** | **What do we check before this specific AI feature ships — and again at every significant change?** |

SAILORS is designed to be used at the feature level: a single RAG pipeline, a single tool-calling capability, a single LLM-backed endpoint, not the whole system or the whole agent architecture. It's meant to be fast enough to run in a design review, not just a compliance exercise.

---

## The Framework

| Letter | Principle | What it checks |
|---|---|---|
| **S** | Sanitize all inputs | Are user/tool inputs validated, encoded, and bounded before reaching the model? |
| **A** | Access controls at retrieval | Does retrieval (RAG, tool calls, memory) respect the requesting user's actual permissions? If retrieval is itself another agent's output, this becomes a MAESTRO question — cross-agent trust isn't a single-capability fix. |
| **I** | Inspect and filter outputs | Is model output checked before it's rendered, executed, or passed downstream? |
| **L** | Least privilege for tools | Does the capability hold only the permissions it needs, nothing more? Includes resource-usage scope — token exhaustion and unbounded tool calls are permission problems, not input problems. |
| **O** | Override gate for humans (action + scope) | Is there a human checkpoint before (1) a consequential action fires, and (2) any expansion in the capability's scope or permissions during a session? |
| **R** | Record every action | Is there an audit trail sufficient to reconstruct what happened and why? If the agent writes its own log, the log is only as trustworthy as the agent — route logs through a channel the capability can't modify, where possible. |
| **S** | System prompt hardening | Is the system prompt resistant to injection, leakage, and override attempts? |

---

## Mapping to Existing Standards

SAILORS is cross-referenced against:
- OWASP Top 10 for LLM Applications
- OWASP Top 10 for Agentic Applications (the "Agentic Top 10")
- MITRE ATLAS tactics (where applicable at the capability level)

*(Full mapping table: see `/mapping`)*

---

## How to Use It

1. Identify the AI capability being shipped (a feature, not a full system).
2. Walk each SAILORS letter as a checklist item against that capability.
3. Flag gaps as findings, prioritize by exploitability and blast radius.
4. Re-run at each significant capability change, not just once at launch.

A worked example is included in `/examples`.

## SAILORS-Verify (PoC Scanner)

A lightweight proof-of-concept scanner that runs SAILORS' seven checks against real Python code. Covers 5 of 7 checks (S, A, L, O, R) via pattern matching. Honestly documents what it can't yet catch (I, system prompt hardening, and three refined sub-checks that need cross-file context). Not full static analysis — a starting point for a manual review, not a replacement for one.

See [`/poc`](poc) for the scanner, a test file, and example output.

## What Comes After SAILORS

SAILORS covers the design review — what to check before a capability ships. Two frameworks go deeper once the capability is built and deployed:

- **[RAISE](https://open-agent-ai-security.github.io/praxen/guide/RAISE.html)** (Responsible AI Software Engineering) — Steve Wilson's maturity model for how an agent is engineered, secured, tested, and operated. Assesses six categories: Zero Trust, Knowledge Base, Domain Limits, Monitoring, Supply Chain, and AI Red Team.
- **[Praxen](https://open-agent-ai-security.github.io/praxen/)** — open-source agent behavior verifier. Reads an agent's code and deployment state, checks it against a declared policy (Worker Remit), and produces a scored posture report with file:line evidence.

SAILORS asks the questions at design time. RAISE assesses maturity across the agent's engineering. Praxen verifies the controls are actually implemented, after the code exists.

A worked comparison of SAILORS and Praxen/RAISE against a deliberately broken demo agent (FinBot) is in [`/praxen-comparison`](praxen-comparison) — including a [full FinBot analysis report](https://vinayavasu.github.io/SAILORS/praxen-comparison/finbot-analysis-20260721.html).

## Status

SAILORS is an early-stage, open framework. It's being actively used and refined in practitioner threat-modeling work. Feedback, critique, and real-world application notes are genuinely wanted, especially from anyone applying STRIDE or MAESTRO today who's hit the same capability-level gap.

## Changelog

**July 2026**
**Two checks revised after practitioner review from Harshad Sadashiv Kadam:**
- **O** now covers two conditions instead of one: gating the action itself, and separately gating any mid-session growth in the capability's scope or permissions.
- **A** now includes an explicit hand-off rule: when retrieval is another agent's output rather than a static lookup, defer to MAESTRO instead of stretching A to cover it.

**Three refinements following review from Shivam Dhar:**
- L now explicitly covers resource-usage scope — token exhaustion and unbounded tool calls are permission problems, not input problems.
- R now includes a log-trust note for agent-written audit trails.
- The framing question now reflects continuous re-running, not just pre-ship review.

## Roadmap

- **SAILORS-Verify** (`/poc`) is live — covers 5 of 7 checks (S, A, L, O, R) as a pattern-matching scanner. Next: AST-based analysis for cross-file checks (A's MAESTRO hand-off, O's scope-expansion gate, R's log-trust note), and coverage for I and system prompt hardening.
- **CI integration** — exploring how to run SAILORS-Verify as a pre-merge gate, not just a standalone script.
- **AIBOM pairing** — exploring how SAILORS could pair with an AI Bill of Materials, using capability discovery to auto-trigger a review when something new ships.

## Author

**Vinaya Vasudevan**, AI Security Engineer, CAISP, SANS AIS247
Portfolio: [vinayavasu.github.io](https://vinayavasu.github.io)
Writing: [Prompt to Patch](https://prompt-to-patch-vinaya.hashnode.dev)

## Contributing

Issues and PRs welcome. If you're using SAILORS on a real capability review, an example write-up (even anonymized) is one of the most useful contributions right now.

## License

MIT
