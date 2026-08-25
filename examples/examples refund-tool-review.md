# Worked Example: Support Assistant — New Refund Tool

> **A filled-in SAILORS review for one AI capability.** This is what a completed review looks like when a team spends 30 minutes running the seven checks on a real feature change. Use it as a reference when you run your own.

This is a synthetic capability, but every finding maps to a real pattern seen in agentic assistants that call financial tools. Names, thresholds, and evidence are illustrative.

---

## Capability Information

**Capability Name:** Support Assistant - new `refund_tool`

**Owner:** Payments Platform team

**Date:** 2026-08-20

**Reviewers:** Vinaya Vasudevan (security), Priya M. (payments PM), Sam T. (platform)


## AIBOM Snapshot

The AIBOM is what triggered this review. A new tool was added to an existing assistant.

**AIBOM ID / Version:** `support-assistant@2.4.0`
**Change since last review:** `tools` list grew — `refund_tool` added. Nothing else changed. Last SAILORS review was 2026-06-04 at `support-assistant@2.3.1`.

**Model / Provider:** OpenAI, `gpt-4o-2024-08-06`, hosted API
**Data Sources:** support-kb-vector-db, ticket-history-api (read-only, per-user scope), payments-api (new — used by `refund_tool`)
**Tools / Actions:** `lookup_ticket`, `search_kb`, `reply_to_customer`, `refund_tool` (new)
**Agentic Skills / Packages:** none — `refund_tool` is a first-party internal tool, not an MCP or plugin. AST10 companion checklist marked N/A for this review.
**Output Destinations:** support-console web-ui, customer-email (via `reply_to_customer`), payments-api (via `refund_tool`)
**Consequential Actions:** `reply_to_customer` (email send), `refund_tool` (money movement — new consequential action for this capability)

## Threat Assessment (Prerequisite)

**Threat Model Reference:** STRIDE — refreshed 2026-08-19 for the `refund_tool` addition

**Key Threats Identified:**

1. **Tampering / Elevation of Privilege** — a prompt-injected instruction causes the assistant to issue refunds it shouldn't (STRIDE T + E)
2. **Repudiation** — refund is issued, no audit trail ties it to the ticket or the reviewer (STRIDE R)
3. **Information Disclosure** — assistant leaks another customer's ticket detail when scoping the refund (STRIDE I)

**SAILORS Checks Selected Based on Threats:** L, O, R, S(prompt). I is relevant because refund confirmations render in the console and go to customer email.

**Checks Marked N/A (Not Relevant):** A — retrieval scope did not change for this AIBOM diff; last review verified per-user tenant isolation on ticket-history-api. S(sanitize) — input sanitization on user messages did not change; unchanged from previous review.

**Result:** run I, L, O, R, S(prompt). Skip S(sanitize) and A per the trigger matrix.

---

## Check 1: S - Sanitize All Inputs

**Status:** N/A (unchanged from `support-assistant@2.3.1` review)

**Evidence:** Input sanitization layer (`prompt_scrub_v2`) applies to all user messages before they reach the model. No change since last review.

**Findings:** none for this review — see previous review notes.

---

## Check 2: A - Access Controls at Retrieval

**Status:** N/A (unchanged from `support-assistant@2.3.1` review)

**Evidence:** ticket-history-api enforces `user_id = requesting_user.id` at the API gateway. Vector store queries are per-tenant. Unchanged.

**Findings:** none for this review.

---

## Check 3: I - Inspect and Filter Outputs

**Status:** PARTIAL

**Evidence:** Existing output filter checks for PII patterns in `reply_to_customer` responses. **Gap:** the refund confirmation message rendered in the support console goes through the same filter, but the internal call to `refund_tool` does not — the tool arguments (amount, account_id, reason) are passed straight from the model output without validation.

**Findings:** `refund_tool` accepts whatever amount the model emits, up to the tool's own cap of $10,000. No output-side sanity check (e.g., "does this amount match the ticket's original charge?") before the tool call fires.

**Severity:** Medium

**Release Blocker:** No — the O check below catches this via human approval. But it should be fixed in the next sprint. Recommend adding an amount-vs-original-charge sanity check in the tool wrapper.

**Owner:** Sam T. **Due Date:** 2026-09-15

---

## Check 4: L - Least Privilege for Tools

**Status:** FAIL

**Evidence:** The `refund_tool` credential is a single service account (`svc-support-refunds`) with `payments:refund:*` scope. It can refund any transaction on any account in the payments-api, not just the account tied to the ticket the assistant is working on.

**Findings:** Tool credential is not scoped to the requesting user's account. If prompt injection or a bad reasoning chain caused the assistant to call `refund_tool` with `account_id=other_customer_id`, the tool would happily process it. The API accepts the call because the service account has universal refund scope.

**Severity:** High

**Release Blocker:** **Yes**

**Owner:** Sam T. **Due Date:** must be fixed before ship

**Note:** Fix is to derive a short-lived per-request credential that carries `account_id` scope from the ticket context, and reject any `refund_tool` call where the `account_id` argument doesn't match the credential's scope. Token exhaustion and unbounded tool calls are permission problems, not input problems — this is exactly that pattern.

---

## Check 5: O - Override Gate for Humans (Action + Scope)

**Status:** FAIL

**Evidence:**

- **Action gate:** `refund_tool` has a `require_approval` flag. It is set to `true` only for refunds above $500. Below that, the assistant can call the tool autonomously.
- **Scope gate:** No mid-session scope-expansion gate. Once a user is in a support session, the assistant can call any tool in its list including `refund_tool`, without any explicit user-in-the-loop confirmation on "you are about to issue a refund."

**Findings:**

1. The $500 threshold was set by engineering, not by risk. Nothing about $499 is safe.
2. The customer sees the refund appear but never confirms "yes, refund this."
3. No approval gate for the *first* refund in a session — the human-in-the-loop only sees a refund after it has already happened.

**Severity:** Critical

**Release Blocker:** **Yes**

**Owner:** Priya M. **Due Date:** must be fixed before ship

**Note:** Both parts of O must pass. Action gate is partial (threshold-based, not risk-based). Scope-expansion gate is missing. Fix requires (a) a human confirmation step on any `refund_tool` call, and (b) explicit "you are about to authorize a refund" confirmation surfaced to the customer or the support agent in-session.

---

## Check 6: R - Record Every Action

**Status:** PASS

**Evidence:** All tool calls, including `refund_tool`, are logged to `audit-log-service` via a side-channel that the assistant cannot modify. Log entries include ticket_id, user_id, tool_name, tool_args, response, and timestamp. Retention is 7 years for payments-related events. Confirmed by pulling a sample log for the pilot test refunds.

**Findings:** none — logging is one of the strongest parts of this capability. The audit trail is sufficient to reconstruct any refund and tie it to the ticket and reviewer.

**Severity:** N/A

**Release Blocker:** No

---

## Check 7: S - System Prompt Hardening

**Status:** PASS (with note)

**Evidence:** System prompt was re-tested against an extraction suite (prompt-injection corpus, plus three custom probes attempting to override the "refunds require approval" instruction). Prompt held. No credentials in the prompt. Tool schemas are exposed but do not contain sensitive detail.

**Findings:** The prompt's language around "refund_tool should only be called after confirming the ticket's refund policy" is guidance, not enforcement. If L and O were not fixed, a prompt-injected assistant could ignore this and the tool would still fire. **The system prompt is not a control substitute for L and O.**

**Severity:** Info

**Release Blocker:** No — but if L and O are ever relaxed in the future, this note becomes a release blocker.

---

## Companion Checklist: OWASP Agentic Skills Top 10 (AST10)

**Applicability:** No — this capability does not use agentic skills, MCP servers, or plugins. `refund_tool` is a first-party internal tool.

**Section marked N/A.**

---

## Summary

**Total Checks:** 7

**Checks Selected (Based on Threat Assessment):** 5 (I, L, O, R, S-prompt)

**Checks Marked N/A:** 2 (S-sanitize, A — unchanged since last review)

**Passed:** 2 (R, S-prompt)
**Failed:** 2 (L, O)
**Partial:** 1 (I)
**N/A:** 2

**AST10 companion checklist:** N/A

### Top Risks Identified

1. **Unscoped refund credential (L)** — the tool can refund any account, not just the one on the ticket. Prompt injection or reasoning error → unauthorized refunds.
2. **No first-refund human gate (O)** — customer or support agent never explicitly authorizes the refund before it fires. Any autonomous call below $500 is a silent action.
3. **No amount sanity check on tool args (I)** — the model can emit any amount up to $10k and the tool wrapper accepts it without cross-checking the ticket.

### Required Fixes Before Release

1. **Per-request scoped credential for `refund_tool`** — Owner: Sam T. — Due: before ship. Blocks L.
2. **Human-in-the-loop confirmation on every `refund_tool` call** — Owner: Priya M. — Due: before ship. Blocks O.
3. **Amount-vs-original-charge sanity check in the tool wrapper** — Owner: Sam T. — Due: 2026-09-15. Not a blocker, but next-sprint.

### Accepted Risks

None accepted at this review. All findings must be closed or explicitly re-classified as accepted before ship.

## Final Decision

- [x] **BLOCK** — Do not ship until L and O are resolved

**Rationale:** Two release blockers, both on the checks that specifically govern consequential actions. Money-movement capabilities cannot ship with a tool credential broader than the requesting user's scope, or without a human gate on the first action. R and S-prompt are strong, which is why this is a fixable BLOCK, not a redesign.

**Sign-off:** Vinaya Vasudevan, 2026-08-20

---

## Next Review Trigger

This capability should be re-reviewed with SAILORS when the AIBOM changes materially. Specifically:

- [ ] New model or provider is used
- [ ] New retrieval source is added
- [ ] New tool or API is connected
- [ ] New or updated agentic skill package, MCP server, or plugin is added or upgraded
- [ ] Permissions are expanded (e.g., `refund_tool` scope broadens)
- [ ] New autonomous or consequential action is added
- [ ] System prompt is materially changed
- [ ] Output channel changes
- [ ] Memory or vector store changes
- [ ] Incident or near miss occurs

**Next scheduled review date:** On next AIBOM change. Immediate follow-up review scheduled for 2026-09-01 to verify the two blocker fixes before ship.

---

## What this example is meant to show

- **The trigger matrix in action.** The AIBOM change (one new tool) meant we ran 5 of 7 checks, not all 7. That is the point.
- **A realistic BLOCK decision.** Two fails on the checks that matter for money movement. R and S-prompt PASS. This is not a broken capability — it's a fixable one.
- **What "evidence" looks like.** Not "we thought about it" — specific credentials, thresholds, sample log pulls, extraction-test results.
- **How AST10 is handled when N/A.** Documented as not applicable, with a reason. That is itself a security decision.
- **How to write findings.** Each finding says what is wrong, why it's a problem, and what the fix looks like. Severity is assigned. Ownership is assigned. Due date is assigned.

If you run SAILORS on one of your capabilities and want to contribute an anonymized write-up like this back to the project, see [CONTRIBUTING.md](../CONTRIBUTING.md).
