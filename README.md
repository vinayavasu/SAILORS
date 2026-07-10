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
| **SAILORS** | **Individual AI capabilities** | **What do we check before this specific AI feature ships?** |

SAILORS is designed to be used at the feature level: a single RAG pipeline, a single tool-calling capability, a single LLM-backed endpoint, not the whole system or the whole agent architecture. It's meant to be fast enough to run in a design review, not just a compliance exercise.

---

## The Framework

| Letter | Principle | What it checks |
|---|---|---|
| **S** | Sanitize all inputs | Are user/tool inputs validated, encoded, and bounded before reaching the model? |
| **A** | Access controls at retrieval | Does retrieval (RAG, tool calls, memory) respect the requesting user's actual permissions? |
| **I** | Inspect and filter outputs | Is model output checked before it's rendered, executed, or passed downstream? |
| **L** | Least privilege for tools | Does the capability hold only the permissions it needs, nothing more? |
| **O** | Override gate for humans | Is there a human-in-the-loop checkpoint for consequential actions? |
| **R** | Record every action | Is there an audit trail sufficient to reconstruct what happened and why? |
| **S** | System prompt hardening | Is the system prompt resistant to injection, leakage, and override attempts? |

---

## Mapping to Existing Standards

SAILORS is cross-referenced against:
- OWASP Top 10 for LLM Applications
- OWASP Top 10 for Agentic Applications (the "Agentic Top 10")
- MITRE ATLAS tactics (where applicable at the capability level)

*(Full mapping table: see `/mapping`, in progress.)*

---

## How to Use It

1. Identify the AI capability being shipped (a feature, not a full system).
2. Walk each SAILORS letter as a checklist item against that capability.
3. Flag gaps as findings, prioritize by exploitability and blast radius.
4. Re-run at each significant capability change, not just once at launch.

A worked example is included in `/examples`.

---

## Status

SAILORS is an early-stage, open framework. It's being actively used and refined in practitioner threat-modeling work. Feedback, critique, and real-world application notes are genuinely wanted — especially from anyone applying STRIDE or MAESTRO today who's hit the same capability-level gap.

## Author

**Vinaya Vasudevan**, AI Security Engineer, CAISP, SANS AIS247
Portfolio: [vinayavasu.github.io](https://vinayavasu.github.io)
Writing: [Prompt to Patch](https://prompt-to-patch-vinaya.hashnode.dev)

## Contributing

Issues and PRs welcome. If you're using SAILORS on a real capability review, an example write-up (even anonymized) is one of the most useful contributions right now.

## License

MIT
