# SAILORS OWASP Coverage Matrix

This document shows what SAILORS covers directly, what it partially covers, and what it does not cover. For the risks SAILORS does not cover, we list companion controls that teams should use alongside SAILORS.

SAILORS is a design-time review for a single AI capability. It is not a complete AI security program. Use this matrix to understand the boundary and know what else you need.

## OWASP LLM Top 10 (2026) Coverage

| OWASP 2026 | SAILORS Check | Coverage | Companion Control (if needed) | Layer |
|---|---|---|---|---|
| LLM01: Prompt Injection (#1) | S - Sanitize inputs | Direct | Input firewalls, runtime prompt injection detection | Design-time + runtime |
| LLM02: Sensitive Information Disclosure (#2) | A - Access controls at retrieval | Direct | Data loss prevention, memory system isolation | Design-time + runtime |
| LLM03: Excessive Agency (#3) | L + O - Least privilege + Override gate | Direct | Runtime action monitoring, permission scopes | Design-time + runtime |
| LLM04: Supply Chain (#4) | None | Companion | AIBOM, SBOM scanning, model provenance verification, MCP server vetting | Design-time (separate process) |
| LLM05: Data and Model Poisoning (#5) | None | Companion | Training data audit, RAG source validation, fine-tuning integrity checks | Design-time (ML-specific) |
| LLM06: Unbounded Consumption (#6) | L - Least privilege (partial: resource-usage scope) | Partial | Rate limiting, token budgets, cost caps, circuit breakers | Runtime (design decision to implement) |
| LLM07: Misinformation (#7) | I - Inspect outputs (partial) | Partial | Output grounding, fact-checking, source citation, RAG grounding verification | Design-time + runtime |
| LLM08: Hidden Context Exposure (#8) | S - System prompt hardening | Direct | Context window isolation, tool schema obfuscation, developer instruction separation | Design-time |
| LLM09: Vector and Embedding Weaknesses (#9) | A - Access controls at retrieval | Direct | Vector store ACLs, tenant isolation, embedding inversion detection | Design-time + runtime |
| LLM10: Improper Output Handling (#10) | I - Inspect outputs | Direct | Output validation, sink sanitization, content security policy | Design-time |

**Summary:** SAILORS provides direct coverage for 6 of 10 LLM Top 10 categories, partial coverage for 2, and companion controls for 2.

## OWASP Agentic Top 10 (2026) Coverage

| OWASP Agentic 2026 | SAILORS Check | Coverage | Companion Control (if needed) | Layer |
|---|---|---|---|---|
| ASI01: Agent Goal Hijack | S - Sanitize inputs + S(prompt) | Direct | Runtime instruction detection, content filtering | Capability-level |
| ASI02: Tool Misuse and Exploitation | L - Least privilege for tools | Direct | Tool schema validation, runtime tool monitoring | Capability-level |
| ASI03: Identity and Privilege Abuse | A - Access controls at retrieval | Direct | Identity management, credential rotation, tenant isolation | Capability-level |
| ASI04: Agentic Supply Chain Vulnerabilities | None | Companion | AIBOM, dependency scanning, MCP server verification, plugin signing | Architecture-level |
| ASI05: Unexpected Code Execution | L + O (partial) | Partial | Code execution sandboxing, AST analysis, runtime code monitoring | Capability-level (partially) |
| ASI06: Memory and Context Poisoning | R - Record every action (partial) | Partial | Memory validation, memory integrity checks, context sanitization | Capability-level (partially) |
| ASI07: Insecure Inter-Agent Communication | None | Companion | MAESTRO (cross-agent trust), mTLS, message signing, agent identity verification | Architecture-level (MAESTRO) |
| ASI08: Cascading Failures | R - Record every action (partial) | Partial | Circuit breakers, failure isolation, graceful degradation, health checks | Architecture-level + runtime |
| ASI09: Human-Agent Trust Exploitation | I + O - Inspect outputs + Override gate | Direct | Transparency indicators, trust scoring, human-in-the-loop verification | Capability-level |
| ASI10: Rogue Agents | R - Record every action (partial) | Partial | Runtime behavioral monitoring, anomaly detection, kill switches | Runtime |

**Summary:** SAILORS provides direct coverage for 4 of 10 Agentic Top 10 categories, partial coverage for 4, and companion controls for 2.

## How to Use This Matrix

1. Run SAILORS on your AI capability to cover the direct and partial categories.
2. Check the companion control column for risks SAILORS does not fully cover.
3. Ensure those companion controls are owned by the right team (DevSecOps, platform engineering, ML security, architecture).
4. Document in your SAILORS review which companion controls are in place and which are missing.

## Companion Control Owners

| Gap Area | Companion Control | Who Owns It |
|---|---|---|
| Supply Chain (LLM04, ASI04) | AIBOM, dependency scanning, model provenance, MCP server vetting | DevSecOps team |
| Data Poisoning (LLM05) | Training data audit, RAG source validation, fine-tuning integrity | ML/security team |
| Unbounded Consumption (LLM06) | Rate limiting, token budgets, cost caps, circuit breakers | Platform engineering |
| Misinformation (LLM07) | Output grounding, fact-checking, source citation | Product team |
| Code Execution (ASI05) | Sandboxing, AST analysis, runtime code monitoring | Security engineering |
| Memory Poisoning (ASI06) | Memory validation, integrity checks, context sanitization | Security engineering |
| Inter-Agent Communication (ASI07) | MAESTRO, mTLS, message signing, agent identity | Architecture team |
| Cascading Failures (ASI08) | Circuit breakers, failure isolation, graceful degradation | Platform engineering |

## Sources

- [OWASP LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [OWASP Agentic Top 10 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [Infosecurity Magazine analysis (Aug 5, 2026)](https://www.infosecurity-magazine.com/news/prompt-injection-llm-risk/)
- [Invicti analysis (Aug 5, 2026)](https://www.invicti.com/blog/web-security/owasp-llm-top-10-2026-whats-new)
