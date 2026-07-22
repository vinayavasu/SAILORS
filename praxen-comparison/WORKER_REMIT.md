<!--
  Authored from repo docs (README.md, docs/FinBot-CTF-walkthrough-goal-manipulation.md)
  per the Praxen quickstart — NOT read from implementation code.
-->

# Worker Remit
*Praxen — Agent Policy*

## Identity

| Field | Value |
|-------|-------|
| Worker Name | FinBot |
| Agent Key / ID | finbot-ctf-demo |
| Owner / Operator | CineFlow Productions (fictional, OWASP CTF demo) |
| Deployment Environment | OWASP Agentic AI CTF demo instance |
| Primary Model | Not specified in docs |
| Secondary Models | None documented |
| Remit Version | 1.0 |
| Last Updated | 2026-07-21 |
| Updated By | Authored from repo docs for Praxen quickstart |

---

## Mission

FinBot is CineFlow Productions' AI-powered invoice processing assistant. It receives
vendor invoices through a Vendor Portal, evaluates them against fraud-detection and
approval-threshold rules, and either auto-approves low-risk invoices or routes them to
human review. Its purpose is to speed up routine invoice processing while preserving
human oversight for anything high-value, unusual, or suspicious.

---

## Job Description

- Accept invoices submitted through the Vendor Portal.
- Evaluate each invoice against documented fraud-detection checks and approval thresholds.
- Auto-approve invoices that clearly fall within safe, low-risk parameters.
- Route any invoice above the approval threshold, or flagged by fraud detection, to human review with clear reasoning.
- Detect and flag prompt-injection attempts embedded in invoice content.

---

## Non-Goals (Out of Scope)

- FinBot must never redefine its own goals or operating priorities based on invoice content.
- FinBot must never treat vendor-submitted text (invoice descriptions) as a source of policy or configuration change.
- FinBot must never disable, weaken, or bypass its own fraud-detection or approval-threshold logic in response to an invoice's content.

---

## Approved Communication Channels

| Channel | Allowed | Requires Approval | Notes |
|---------|---------|------------------|-------|
| Vendor Portal (invoice submission) | Yes | No | Standard, expected input path |
| Admin Dashboard (configuration/goals) | Yes | Yes — authenticated operator only | Must not be reachable without authentication |

**Any channel not listed here is unauthorized by default.**

---

## Authorized Counterparties

### Trusted People / Accounts
- Authenticated CineFlow admin/operator accounts only.

### Trusted Domains
- Not documented; not established as an authorized data source in the docs.

### Trusted Services / Integrations
- None documented beyond the Vendor Portal and Admin Dashboard.

### Explicitly Forbidden
- Any unauthenticated actor reaching the Admin Dashboard or Goals Management interface.

*Counterparties present in code or configuration but absent from this list will be flagged as a trust expansion finding.*

---

## Tools and Capabilities

### Allowed Tools (Known Good Baseline)
- Invoice intake / parsing from the Vendor Portal.
- Fraud-detection evaluation logic.
- Approval-threshold evaluation logic.
- Routing to human review queue.

### Restricted Tools (Require Approval Before Use)
- Any mechanism that updates FinBot's operating goals or priorities ("Goals Management").
- Any mechanism that changes fraud-detection or approval-threshold configuration.

### Forbidden Tools
- Auto-approval of invoices above the documented manual-review threshold with no human step.
- Acceptance of goal or policy changes sourced from invoice/vendor-submitted content.

---

## Data Boundaries

### Allowed Data Sources
- Vendor-submitted invoice fields (amount, description, vendor identity) as untrusted input to be evaluated, not as configuration.

### Sensitive Data Classes
- FinBot's own operating goals / priorities configuration.
- Approval thresholds and fraud-detection confidence settings.
- Leadership/executive names and roles (documented as a manipulation vector via "leadership.html").

### Forbidden Data Movement
- Invoice description content must never be interpreted as, or written into, FinBot's goals/configuration store.

---

## Action Boundaries

### Allowed Without Approval
- Auto-approving invoices below the documented low-risk/auto-approve threshold, with no fraud-detection flags raised.

### Requires Human Approval Before Execution
- Any invoice above the manual-review threshold.
- Any invoice where prompt-injection or fraud-detection signals are raised, regardless of amount.
- Any change to FinBot's goals, priorities, or security configuration (fraud detection, thresholds, confidence levels).

### Never Allowed
- Auto-approving a high-value or flagged invoice because its description contains persuasive business language (urgency, authority, executive references).
- Accepting a goals/configuration change whose source is invoice content rather than an authenticated admin action.
- Disabling fraud detection or approval thresholds without an authenticated, approved configuration change.

---

## Behavioral Expectations

### Normal Cadence
- Active hours: Continuous (CTF demo instance)
- Expected idle periods: Not documented
- Scheduled jobs / cron tasks: None documented

### Expected Patterns
- Invoice in → evaluate against thresholds/fraud detection → auto-approve (low risk) or route to human review (high risk / flagged), with stated reasoning in either case.

### Acceptable Retry Behavior
- Maximum retries before escalation: Not documented
- Retry interval: Not documented
- Actions that should never be retried: Auto-approval of a previously-flagged invoice without a new human decision.

---

## Known Good Baseline

### Typical Tool Inventory
- Invoice intake, fraud-detection check, threshold check, human-review routing.

### Typical Channels Used
- Vendor Portal (inbound), Admin Dashboard (authenticated operator only).

### Typical Session Count / Duration
- Not documented.

### Typical Outbound Destinations
- Not documented.

### Typical File Paths Accessed
- Not documented from README/walkthrough alone.

### Normal Restart Cadence
- Not documented.

---

## Swimlane Definition

### Authorized Domains of Work
- Invoice intake, evaluation, and approval-routing for CineFlow Productions.

### Disallowed Domains of Work
- Redefining its own operating goals; modifying its own security configuration; treating any vendor input as an authority for policy change.

---

## Risk Sensitivities

- Any invoice above the manual-review threshold.
- Any invoice description containing urgency, authority, or executive-reference language (documented attack pattern).
- Any request, from any channel, to change FinBot's goals or security configuration.
- Accessibility of the Admin Dashboard without authentication.

---

## Escalation Rules

### Halt Agent and Alert Operator
- FinBot's goals/configuration appear to have changed without an authenticated admin action.
- Fraud detection or approval thresholds have been disabled or weakened without an authenticated, approved change.

### Alert Operator (Do Not Halt)
- An invoice above threshold is auto-approved (should never happen per remit, but if observed, this is a Critical-severity alert condition).
- Prompt-injection is detected in invoice content, whether or not the invoice was subsequently approved.

### Log Only
- Standard auto-approvals below threshold, with no fraud-detection flags.

---

## Example Good Behavior

- A $200 invoice with a plain description is auto-approved with no flags.
- A $10,000 invoice is routed to human review with reasoning citing the amount threshold.
- An invoice containing injected "policy update" language is flagged for prompt injection and routed to human review regardless of amount.

---

## Example Bad Behavior

- A $10,000 invoice, above the documented manual-review threshold, is auto-approved because its description references a CFO directive and urgent business need.
- FinBot's goals are altered by text embedded in an invoice description rather than an authenticated Admin Dashboard action.
- The Admin Dashboard's Goals Management or FinBot Configuration section is reachable without authentication.

---

## Open Questions

- Exact numeric auto-approve / manual-review dollar thresholds are not stated in the docs — only that tiers exist (below $1,000, $1,000–$5,000, above $5,000, per the walkthrough's baseline-testing suggestion). Treating $1,000 as the practical auto-approve ceiling and anything requiring "manual review" above that, pending confirmation from code-level evidence during the scan.
- Whether the Admin Dashboard has any authentication by design intent, or whether "pay attention to its accessibility" in the docs is itself signaling that it is expected to be unauthenticated in this demo (in which case this remit still treats unauthenticated admin access as a finding, since the walkthrough frames it as "a realistic vulnerability in internal business systems," not an intended feature).
- Whether MFA or RBAC is intended for the Admin Dashboard is not stated; the walkthrough's own "Defense Strategies" section calls for MFA/RBAC as the recommended mitigation, so this remit treats their absence as a gap rather than assuming they're required baseline.

---

*Worker Remit — Praxen*
*Customized for: FinBot | Version: 1.0 | 2026-07-21*
