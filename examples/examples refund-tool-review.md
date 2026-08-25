# Worked Example: New Refund Tool Added to a Support Assistant

**Capability:** A customer support assistant that already looks up order history. A refund tool was just added to it — the assistant can now issue refunds under a configured dollar threshold without human approval.

This walks through what changed in the AIBOM, which SAILORS checks the trigger matrix said to re-run, and what the thirty-minute review actually found. The full walkthrough of the original assistant is in [`refund-capability-walkthrough.md`](refund-capability-walkthrough.md).

---

## What changed in the AIBOM

Two fields moved:

- `tools` — added `refund_tool` (was: `order_lookup` only).
- `outputs` — added `payment_system` as a downstream sink (was: `chat_ui` only).

That's it. Same model, same data sources, same system prompt.

## Which checks the trigger matrix said to re-run

New tool + new output sink → re-run **L, O, I**. Not all seven. That's the whole point of the trigger matrix — a small change gets a small review.

I also re-ran **R** for a sanity check on the audit trail, because the refund is a money-moving action and I wanted the log entries in one place. S (both of them) and A did not need re-running.

---

## L — Least privilege for tools

The refund tool was wired to the same API credentials as the internal admin panel. The admin panel has no upper bound on refund amount. Convenient to build, bad idea to ship.

**Status:** FAIL. Release blocker.

**Fix:** Give the refund tool its own credential, hard-capped at the configured threshold at the API-gateway level. The model should be architecturally incapable of issuing a refund above the threshold, not just told not to.

---

## O — Override gate for humans

The threshold existed in the documentation. It did not exist in the code. The model could be talked into recommending a refund above it, and the system would just execute it.

**Status:** FAIL. Release blocker.

**Fix:** Enforce the threshold at the system level. Anything above it routes to a queue for human approval, regardless of how confident the model sounds. And on the scope side: if this same assistant later gets handed store credit or address changes as new capabilities, those need their own approval gates. Approval for refunds does not inherit to anything else.

---

## I — Inspect and filter outputs

The refund amount was pulled straight from the model's output and handed to the payment system with no bounds checking at all. Not a well-formed-number check, not an "is this within policy" check, nothing.

**Status:** PARTIAL. Blocker for the money path, fine for chat.

**Fix:** Before any refund executes, validate that the output is a well-formed number, within policy bounds, and matches either the order total or a documented partial-refund policy. This is the belt-and-suspenders line: even if the prompt gets tricked, the bounds check downstream catches it.

---

## R — Record every action

Only the final refund amount and timestamp got logged. The customer's original message, the retrieved order data, and the model's stated reasoning were all discarded.

**Status:** PARTIAL.

**Fix:** Log the full chain — customer message, retrieved order data, model output and reasoning, final action. That's the difference between "we don't know what happened" and "here's exactly what happened and why," six weeks later when nobody remembers the ticket.

And route these logs somewhere the capability itself cannot rewrite. If the agent writes its own log, the log is only as trustworthy as the agent.

---

## Summary

Three checks re-run in about thirty minutes. Two blockers (L and O), one partial that's a blocker for the money path (I), one partial on the audit trail (R).

**Final decision: BLOCK.** Do not ship this refund tool until L and O are fixed at the system level, and until I validates amounts before the payment system sees them.

None of these findings are exotic. Scoped credentials, threshold enforcement, output bounds checking, full logging — standard security practice, applied to a place teams often forget to apply it, because "it's just a chatbot" makes it feel lower-risk than it actually is.

This is what SAILORS is for. The scanner missed I (it doesn't cover output inspection yet). The AIBOM diff told me which three checks mattered. A human review closed the loop in half an hour.

---

**Related:**
- [`refund-capability-walkthrough.md`](refund-capability-walkthrough.md) — full walkthrough of the original assistant, teaching each check in prose.
- [`../templates/sailors-review-template.md`](../templates/sailors-review-template.md) — the fillable version of what's above.
- [`../docs/aibom-trigger.md`](../docs/aibom-trigger.md) — how the trigger matrix picks the check subset.
