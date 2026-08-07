---
name: update-model-and-contract-test
description: Workflow command scaffold for update-model-and-contract-test in tradestation-sdk-python.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /update-model-and-contract-test

Use this workflow when working on **update-model-and-contract-test** in `tradestation-sdk-python`.

## Goal

Update a Pydantic model to accept new or changed fields and ensure contract tests cover the new behavior.

## Common Files

- `tradestation/models/orders.py`
- `tradestation/models/streaming.py`
- `tradestation/order_executions.py`
- `tests/test_pydantic_contract.py`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Edit the relevant Pydantic model to accept new/optional fields.
- Update or add logic in the implementation to handle the new model behavior.
- Update or add contract tests to verify the new/changed model behavior.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.