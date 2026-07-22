**SAILORS vs. Praxen - a practitioner comparison**



This folder holds a real, run-through-completion comparison between SAILORS and Praxen (Steve Wilson's agent behavior verifier, built on the RAISE framework), done against FinBot, the OWASP Agentic AI CTF demo agent.

**What's here:**

**WORKER_REMIT.md** — the policy document authored from FinBot's own docs (not its code), per Praxen's quickstart instructions
**finbot-analysis-20260721.html / .txt** — the actual rendered Praxen report: RAISE posture 0.60/5 (Absent), 5 findings, all with file:line evidence

The relationship, in short: SAILORS is a pre-ship checklist -> seven questions run during design review, before an AI capability exists. Praxen is post-build verification —> it reads deployed code and proves, with evidence, whether the things SAILORS would have asked about are actually there. Same underlying concerns (access control, override gates, audit trails), different point in the lifecycle. Several of FinBot's five findings here map directly to what a SAILORS review would have flagged on paper before any of this code shipped — Praxen is what caught them for real, after the fact, with a score attached.

These are independent findings from running Praxen's public quickstart, not an endorsement or partnership. Full tool and framework credit: Praxen.
