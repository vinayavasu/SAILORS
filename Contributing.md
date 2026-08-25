# Contributing to SAILORS

SAILORS is v1.1 and actively seeking practitioner feedback. If you have used SAILORS on a real capability, or if you want to help sharpen the framework, here are three concrete ways to contribute.

## 1. Send me an anonymized review write-up

**This is the single most useful contribution right now.**

If you have run SAILORS on one of your AI capabilities:

- Fill in the [review template](templates/sailors-review-template.md) for one feature.
- Anonymize company names, product names, and any credentials or thresholds you cannot share. Keep the findings honest.
- Open a pull request adding your write-up to `examples/` (e.g., `examples/your-capability-review.md`).

Alternatively, if you cannot publish it, email a summary to me directly — see the author section in the README. Even feedback like "we tried it, and here is where check X did not fit our workflow" is valuable.

**What I am looking to learn from these:**

- Which of the seven checks were most useful?
- Which felt awkward or ambiguous?
- What was missing? (Did you have to add anything to make the review usable?)
- How long did the review actually take?

See [`examples/refund-tool-review.md`](examples/refund-tool-review.md) for the format and depth I am looking for.

## 2. Try SAILORS-Verify and file a false-positive issue

The proof-of-concept scanner in [`poc/`](poc/) covers 5 of 7 checks using pattern matching. Pattern matching produces false positives.

If you run it on your Python code:

- Open an issue titled `[false positive] <check> — <short description>`.
- Include the code pattern the scanner flagged, and why it is not actually a violation.
- Label the issue `false-positive` (a maintainer will add the label if needed).

This helps prioritize which checks need AST-based analysis first.

## 3. Suggest a companion control for a coverage gap

The [coverage matrix](docs/owasp-coverage-matrix.md) lists risks that SAILORS covers only partially, or that require a companion control (supply chain, data poisoning, unbounded consumption, inter-agent communication, and cloud AI service configuration).

If you have a companion control that works for your team:

- Open an issue titled `[companion control] <gap area> — <what you use>`.
- Say briefly: what tool or process fills the gap, which team owns it, what evidence you record.
- If it is generalizable, propose an update to the matrix in a pull request.

## Code of conduct

Be direct. Be kind. Names and quotes stay unless the person asks otherwise.

## Licensing

By contributing, you agree that your contributions will be licensed under the same MIT license that covers the project.
