# AIBOM Trigger for SAILORS Reviews

## Core Concept

AIBOM (AI Bill of Materials) tells you what AI capabilities exist and when they change. SAILORS tells you what to review before that capability ships.

AIBOM is the trigger. SAILORS is the review. They are separate things that work together.

---

## How It Works

```
AIBOM identifies an AI capability or a change to one
    |
    v
SAILORS review is triggered for that specific capability
    |
    v
Team runs the 7 checks in a 30-minute design review
    |
    v
Findings are documented in the SAILORS review template
    |
    v
AIBOM review status is updated
    |
    v
Capability ships, ships with fixes, or is blocked
```

---

## Minimal AIBOM Fields

An AIBOM entry for one AI capability should contain at minimum:

| Field | Description | Example |
|---|---|---|
| capability_id | Unique identifier for this capability | cap-001 |
| name | Human-readable name | HR Q&A RAG Bot |
| owner | Person or team responsible | platform-team |
| model_provider | LLM provider | OpenAI |
| model_version | Specific model version | gpt-4o-2024-08-06 |
| system_prompt_ref | Link to stored system prompt | s3://prompts/hr-bot/v3.txt |
| retrieval_sources | List of data sources the capability accesses | ["hr-docs-vector-db", "employee-api"] |
| tools | List of tools/APIs the capability can call | ["send-email", "lookup-policy"] |
| permissions | Permission scopes the capability holds | ["read:hr-docs", "send:email"] |
| output_destinations | Where output goes | ["web-ui", "slack-channel"] |
| human_approval_gates | Where human approval is required | ["before-email-send"] |
| logging | What is logged and where | ["all-actions", "s3://logs/hr-bot/"] |
| risk_tier | Assessed risk level | medium |
| last_reviewed | Date of last SAILORS review | 2026-08-15 |
| review_status | Current review state | approved / pending / blocked |

---

## Example AIBOM Entry (YAML)

```yaml
capability_id: cap-001
name: HR Q&A RAG Bot
owner: platform-team
model_provider: OpenAI
model_version: gpt-4o-2024-08-06
system_prompt_ref: s3://prompts/hr-bot/v3.txt
retrieval_sources:
  - hr-docs-vector-db
  - employee-directory-api
tools:
  - send-email
  - lookup-policy
permissions:
  - read:hr-docs
  - send:email
output_destinations:
  - web-ui
  - slack-hr-channel
human_approval_gates:
  - before-email-send
logging:
  - all-actions
  - s3://logs/hr-bot/
risk_tier: medium
last_reviewed: 2026-08-15
review_status: approved
```

---

## Trigger Events

A SAILORS review should be triggered when any of these AIBOM changes occur:

| Trigger Event | Why It Matters | SAILORS Checks to Re-run |
|---|---|---|
| New AI capability added | Full initial review needed | All 7 checks |
| New model or provider swapped | Different model means different risks, different system prompt behavior | S, I, R, S (system prompt) |
| New retrieval source added | New data means new access control questions | A, I |
| New tool or API connected | New tools mean new permissions and blast radius | L, O, R |
| Permissions expanded | More access means more blast radius | L, O |
| New autonomous or consequential action added | Actions need human gates | O, R |
| System prompt materially changed | Prompt changes affect injection resistance, behavior | S, I |
| Output channel changed | New destination means new filtering needs | I, R |
| Memory or vector store changed | New memory means new retrieval and access questions | A, R |
| Incident or near miss occurred | Something went wrong, re-review to find what was missed | All 7 checks |

---

## Trigger Matrix

Not every change requires all 7 checks. The trigger matrix tells you which checks to re-run based on what changed:

```
                        S   A   I   L   O   R   S(prompt)
New capability          Y   Y   Y   Y   Y   Y   Y
New model/provider      Y   -   Y   -   -   Y   Y
New retrieval source    -   Y   Y   -   -   -   -
New tool/API            -   -   -   Y   Y   Y   -
Permissions expanded    -   -   -   Y   Y   -   -
New consequential action -  -   -   -   Y   Y   -
System prompt changed   Y   -   Y   -   -   -   Y
Output channel changed  -   -   Y   -   -   Y   -
Memory/vector store     -   Y   -   -   -   Y   -
Incident or near miss   Y   Y   Y   Y   Y   Y   Y
```

This means a team that adds a new tool to an existing capability only needs to re-run L, O, and R, not all 7 checks. This makes SAILORS scalable for ongoing changes.

---

## Workflow Integration

### Option 1: Pull Request Trigger (Recommended)

1. Developer opens a PR that adds or changes an AI capability
2. PR template requires updating the AIBOM entry for that capability
3. If AIBOM has changed, SAILORS review template must be filled out
4. Reviewer checks the SAILORS review in the PR
5. PR cannot merge until SAILORS review is approved

### Option 2: CI/CD Gate (Future)

1. Developer opens a PR
2. CI pipeline detects AIBOM changes (diff on aibom.yaml)
3. CI pipeline runs SAILORS-Verify scanner on changed code
4. Scanner output is posted as a PR comment
5. Manual review still required for judgment calls
6. PR cannot merge until SAILORS review is approved

### Option 3: Manual Trigger (Simplest)

1. Team is about to ship an AI capability
2. Someone fills out the AIBOM entry
3. Team runs the SAILORS review template in a 30-minute meeting
4. Results are stored alongside the AIBOM entry
5. Capability ships or is blocked based on the review

Start with Option 3. Move to Option 1 when the team is comfortable. Option 2 is the long-term vision.

---

## Example Workflow

**Scenario:** Team is adding a new tool (send-slack-message) to an existing HR Q&A RAG Bot.

**Step 1:** Developer updates AIBOM entry:

```yaml
# Before
tools:
  - send-email
  - lookup-policy

# After
tools:
  - send-email
  - lookup-policy
  - send-slack-message  # NEW
```

**Step 2:** AIBOM change detected. New tool added. Trigger matrix says: re-run L, O, R.

**Step 3:** Team fills out SAILORS review template for L, O, R only:

- **L (Least Privilege):** Does the Slack tool have minimum permissions? Can it only send to specific channels? PASS if scoped, FAIL if broad access.
- **O (Override Gate):** Is there a human checkpoint before sending Slack messages? PASS if approval gate exists, FAIL if autonomous.
- **R (Record Every Action):** Are Slack messages logged? PASS if logged, FAIL if not.

**Step 4:** Findings documented. If all pass, capability ships. If any fail, fixes required.

**Step 5:** AIBOM review status updated to "approved" with date.

---

## Positioning Statement (Use This When Explaining)

"AIBOM is the inventory. SAILORS is the review. When your AIBOM changes, meaning you added a new AI capability, swapped a model, added a tool, or expanded permissions, SAILORS tells you exactly which checks to re-run before that change ships. Not all 7 checks every time, just the ones affected by the change. This makes SAILORS scalable for teams that ship AI features regularly."

---

## What AIBOM Trigger Is NOT

- It is not a new framework. It is a workflow that connects AIBOM (inventory) to SAILORS (review).
- It is not automated yet. The trigger matrix is a manual reference. CI integration is future work.
- It is not a compliance tool. It is a practical review trigger for engineering teams.

---

## Status

This document is a concept proposal. It has not been validated with real teams yet. The next step is to pilot it with 2 to 3 teams that already use an AIBOM or component inventory and see if the trigger matrix correctly identifies which SAILORS checks to re-run.
