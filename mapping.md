****SAILORS Mapping to Existing Standards**


This is the cross-reference the main README points to. For each SAILORS letter: which OWASP LLM Top 10 (2026) items it addresses, which OWASP Top 10 for Agentic Applications (2026) items it addresses, and where it touches MITRE ATLAS.

A note on confidence: the OWASP mappings below are aligned to the published 2026 taxonomies (OWASP LLM Top 10 2026, OWASP Agentic Top 10 2026). The MITRE ATLAS column is kept at the tactic level, not the technique level. If you're mapping SAILORS into a formal ATLAS-based threat model, treat this column as a starting pointer, not a verified crosswalk, and check against ATLAS directly.

**Combined Mapping Table**

| SAILORS | OWASP LLM Top 10 (2026) | OWASP Agentic Top 10 (ASI) | MITRE ATLAS (tactic-level) |
| :--- | :--- | :--- | :--- |
| **S**: Sanitize all inputs | LLM01: Prompt Injection | ASI01: Agent Goal Hijack | Initial access via adversarial input |
| **A**: Access controls at retrieval | LLM02: Sensitive Information Disclosure, LLM09: Vector and Embedding Weaknesses | ASI03: Identity and Privilege Abuse | Unauthorized data collection |
| **I**: Inspect and filter outputs | LLM10: Improper Output Handling | ASI02: Tool Misuse and Exploitation | Downstream impact from unvalidated output |
| **L**: Least privilege for tools | LLM03: Excessive Agency | ASI02: Tool Misuse and Exploitation, ASI03: Identity and Privilege Abuse | Privilege abuse in the agent's execution environment |
| **O**: Override gate for humans | LLM03: Excessive Agency | ASI01: Agent Goal Hijack, ASI09: Human-Agent Trust Exploitation | Impact mitigation through human checkpoints |
| **R**: Record every action | No direct OWASP mapping | ASI08: Cascading Failures, ASI10: Rogue Agents | Detection and forensic reconstruction |
| **S**: System prompt hardening | LLM08: Hidden Context Exposure | ASI01: Agent Goal Hijack | Defense against instruction manipulation |

**What changed in 2026**
The OWASP LLM Top 10 was updated on August 4, 2026. Key changes that affect this mapping:
**LLM03: ** Excessive Agency moved from #6 to #3. SAILORS L and O checks now map to the #3 risk. OWASP introduced the "Minimal Footprint Principle" which directly aligns with the SAILORS L check philosophy.
**LLM08: ** Hidden Context Exposure (renamed from "System Prompt Leakage") was broadened to cover tool schemas, function schemas, retrieved policy text, developer instructions, and any hidden context in the context window. SAILORS S check already covers this broader scope.

**LLM10: **Improper Output Handling dropped from #5 to #10. SAILORS retains output inspection because a design-time review should catch output handling gaps before they reach production.

R check still has no direct OWASP mapping. OWASP has never had a dedicated logging category in the LLM Top 10. SAILORS includes logging as a design-time release blocker because the decision to log (or not log) is made at design time.

**LLM09:** Vector and Embedding Weaknesses moved from #8 to #9 (was LLM08 in 2025).
**
**Reading this table****
No single SAILORS letter maps to exactly one OWASP item, and that's expected. A gap in access controls (A) can just as easily show up as a data disclosure problem (LLM02) or an identity problem (ASI03), depending on which side of the retrieval you're looking from. SAILORS isn't trying to force a clean one-to-one mapping. It's giving you seven places to look; this table just shows what you're likely to find when you look there.

**What's not covered**
SAILORS provides direct or partial design-time coverage for most capability-level OWASP LLM and Agentic risks. It does not cover risks that require architecture-level or runtime controls (supply chain, data poisoning, unbounded consumption, inter-agent communication). See the coverage matrix for what SAILORS covers directly, what it partially covers, and what companion controls fill the gaps.

**What's not here yet**
This is a first pass, built from the two OWASP taxonomies and a general read of ATLAS's structure, not from a full technique-by-technique crosswalk. If you're using this table for actual compliance mapping or a formal threat model, verify the ATLAS column against the current framework directly before relying on it.

Corrections and refinements welcome, that's exactly the kind of contribution this repo is asking for.
**
**Note on O and A (July 2026)****
O now has two trigger conditions (action-gating and scope-expansion-gating), both still mapping to the same OWASP/ATLAS categories listed above. A carries a new explicit boundary: once retrieval crosses an agent-to-agent trust boundary, the finding belongs in a MAESTRO-level review, not a SAILORS one. Credit to Harshad Sadashiv Kadam for both.

****Note on the 2026 update (August 2026)**
Mapping updated to reflect OWASP LLM Top 10 2026 (released August 4, 2026) and OWASP Agentic Top 10 2026. The previous mapping used 2025 OWASP IDs. See the changelog above for specific changes.
