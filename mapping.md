# SAILORS Mapping to Existing Standards

This is the cross-reference the main README points to. For each SAILORS letter: which OWASP LLM Top 10 items it addresses, which OWASP Top 10 for Agentic Applications (ASI) items it addresses, and where it touches MITRE ATLAS.

A note on confidence: the OWASP mappings below are checked against the published 2026 taxonomies. The MITRE ATLAS column is kept at the tactic level, not the technique level. If you're mapping SAILORS into a formal ATLAS-based threat model, treat this column as a starting pointer, not a verified crosswalk, and check against ATLAS directly.

| SAILORS | OWASP LLM Top 10 | OWASP Agentic Top 10 (ASI) | MITRE ATLAS (tactic-level) |
|---|---|---|---|
| **S**: Sanitize all inputs | LLM01: Prompt Injection | ASI01: Agent Goal Hijack | Initial access via adversarial input |
| **A**: Access controls at retrieval | LLM02: Sensitive Information Disclosure, LLM08: Vector and Embedding Weaknesses | ASI03: Identity and Privilege Abuse | Unauthorized data collection |
| **I**: Inspect and filter outputs | LLM05: Improper Output Handling | ASI02: Tool Misuse and Exploitation | Downstream impact from unvalidated output |
| **L**: Least privilege for tools | LLM06: Excessive Agency | ASI02: Tool Misuse and Exploitation, ASI03: Identity and Privilege Abuse | Privilege abuse in the agent's execution environment |
| **O**: Override gate for humans | LLM06: Excessive Agency | ASI01: Agent Goal Hijack, ASI09: Human-Agent Trust Exploitation | Impact mitigation through human checkpoints |
| **R**: Record every action | LLM02: Sensitive Information Disclosure | ASI08: Cascading Failures, ASI10: Rogue Agents | Detection and forensic reconstruction |
| **S**: System prompt hardening | LLM01: Prompt Injection, LLM07: System Prompt Leakage | ASI01: Agent Goal Hijack | Defense against instruction manipulation |

## Reading this table

No single SAILORS letter maps to exactly one OWASP item, and that's expected. A gap in access controls (**A**) can just as easily show up as a data disclosure problem (LLM02) or an identity problem (ASI03), depending on which side of the retrieval you're looking from. SAILORS isn't trying to force a clean one-to-one mapping. It's giving you seven places to look; this table just shows what you're likely to find when you look there.

## What's not here yet

This is a first pass, built from the two OWASP taxonomies and a general read of ATLAS's structure, not from a full technique-by-technique crosswalk. If you're using this table for actual compliance mapping or a formal threat model, verify the ATLAS column against the current framework directly before relying on it. Corrections and refinements welcome, that's exactly the kind of contribution this repo is asking for.

Corrections and refinements welcome, that's exactly the kind of contribution this repo is asking for.

## Note on O and A (July 2026)

O now has two trigger conditions (action-gating and scope-expansion-gating), both still mapping to the same OWASP/ATLAS categories listed above. A carries a new explicit boundary: once retrieval crosses an agent-to-agent trust boundary, the finding belongs in a MAESTRO-level review, not a SAILORS one. Credit to Harshad Sadashiv Kadam for both.
