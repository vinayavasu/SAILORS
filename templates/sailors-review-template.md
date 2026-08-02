# SAILORS Review Template

**Instructions:** Fill this out during a 30-minute design review before an AI capability ships. One capability per review. If a check is not applicable, mark N/A and explain why. Documenting why something is not applicable is itself a security decision.

---

## Capability Information

## Capability Information

**Capability Name:** [What AI feature is being reviewed?]  
**Owner:** [Who is responsible for this capability?]  
**Date:** [Review date]  
**Reviewers:** [Who is in the review?]  
**AIBOM ID:** [Link to AIBOM entry, if available]  
**Model/Provider:** [Which LLM or model is used?]  
**Data Sources:** [What data does this capability access? RAG, databases, APIs]  
**Tools/Actions:** [What tools can this capability call? What actions can it take?]  
**Output Destinations:** [Where does the output go? UI, API, database, another system]  
**Consequential Actions:** [What actions have real-world impact? Emails, purchases, data modifications]

---

## Check 1: S - Sanitize All Inputs

**Are user and tool inputs validated, encoded, and bounded before reaching the model?**

**Status:** [PASS / FAIL / PARTIAL / N/A]

**Evidence:** [What did you find? What controls exist?]

**Findings:** [What is missing or broken?]

**Severity:** [Critical / High / Medium / Low / Info]

**Release Blocker:** [Yes / No]

**Owner:** [Who fixes this?]
**Due Date:** [When?]

---

## Check 2: A - Access Controls at Retrieval

**Does retrieval (RAG, tool calls, memory) respect the requesting user's actual permissions?**

**Status:** [PASS / FAIL / PARTIAL / N/A]

**Evidence:** [What did you find? What access controls exist?]

**Findings:** [What is missing or broken?]

**Severity:** [Critical / High / Medium / Low / Info]

**Release Blocker:** [Yes / No]

**Owner:** [Who fixes this?]
**Due Date:** [When?]

**Note:** If retrieval is another agent's output, this becomes a MAESTRO question. Flag it and defer to MAESTRO.

---

## Check 3: I - Inspect and Filter Outputs

**Is model output checked before it is rendered, executed, or passed downstream?**

**Status:** [PASS / FAIL / PARTIAL / N/A]

**Evidence:** [What output filtering exists? Guardrails? PII detection?]

**Findings:** [What is missing or broken?]

**Severity:** [Critical / High / Medium / Low / Info]

**Release Blocker:** [Yes / No]

**Owner:** [Who fixes this?]
**Due Date:** [When?]

---

## Check 4: L - Least Privilege for Tools

**Does the capability hold only the permissions it needs, nothing more?**

**Status:** [PASS / FAIL / PARTIAL / N/A]

**Evidence:** [What are the tool scopes? Are they minimal? Are there resource limits?]

**Findings:** [What is missing or broken? Are there excessive permissions?]

**Severity:** [Critical / High / Medium / Low / Info]

**Release Blocker:** [Yes / No]

**Owner:** [Who fixes this?]
**Due Date:** [When?]

**Note:** Token exhaustion and unbounded tool calls are permission problems, not input problems.

---

## Check 5: O - Override Gate for Humans (Action + Scope)

**Is there a human checkpoint before (1) a consequential action fires, and (2) any expansion in the capability's scope or permissions during a session?**

**Status:** [PASS / FAIL / PARTIAL / N/A]

**Evidence:** [What human approval gates exist? What counts as consequential?]

**Findings:** [What is missing or broken? Is scope expansion gated?]

**Severity:** [Critical / High / Medium / Low / Info]

**Release Blocker:** [Yes / No]

**Owner:** [Who fixes this?]
**Due Date:** [When?]

**Note:** This check has two parts. Gating the action itself AND separately gating any mid-session growth in scope or permissions. Both must pass.

---

## Check 6: R - Record Every Action

**Is there an audit trail sufficient to reconstruct what happened and why?**

**Status:** [PASS / FAIL / PARTIAL / N/A]

**Evidence:** [What is logged? Where? Can the agent modify its own logs?]

**Findings:** [What is missing or broken? Are logs trustworthy?]

**Severity:** [Critical / High / Medium / Low / Info]

**Release Blocker:** [Yes / No]

**Owner:** [Who fixes this?]
**Due Date:** [When?]

**Note:** If the agent writes its own log, the log is only as trustworthy as the agent. Route logs through a channel the capability cannot modify, where possible.

---

## Check 7: S - System Prompt Hardening

**Is the system prompt resistant to injection, leakage, and override attempts?**

**Status:** [PASS / FAIL / PARTIAL / N/A]

**Evidence:** [Has the prompt been tested against extraction? Are there credentials in it?]

**Findings:** [What is missing or broken?]

**Severity:** [Critical / High / Medium / Low / Info]

**Release Blocker:** [Yes / No]

**Owner:** [Who fixes this?]
**Due Date:** [When?]

---

## Summary

**Total Checks:** 7
**Passed:** [N]
**Failed:** [N]
**Partial:** [N]
**N/A:** [N]

### Top Risks Identified

1. [Risk 1]
2. [Risk 2]
3. [Risk 3]

### Required Fixes Before Release

1. [Fix 1] - Owner: [Name] - Due: [Date]
2. [Fix 2] - Owner: [Name] - Due: [Date]

### Accepted Risks

1. [Risk that is accepted and why]

### Final Decision

[ ] APPROVE - Ship as-is
[ ] APPROVE WITH FIXES - Ship after listed fixes are completed
[ ] BLOCK - Do not ship until critical findings are resolved
[ ] NEEDS RE-REVIEW - Re-run SAILORS after changes are made

**Sign-off:** [Reviewer name and date]

---

## Next Review Trigger

This capability should be re-reviewed with SAILORS when:

[ ] New model or provider is used
[ ] New retrieval source is added
[ ] New tool or API is connected
[ ] Permissions are expanded
[ ] New autonomous or consequential action is added
[ ] System prompt is materially changed
[ ] Output channel changes
[ ] Memory or vector store changes
[ ] Incident or near miss occurs

**Next scheduled review date:** [Date or "On next significant change"]
