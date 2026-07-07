# Receipt Field Guide

Use concise, reviewable language. A receipt should be useful without exposing private logs or internal systems.

## Required Fields

- `receipt_id`: Stable local identifier for the receipt.
- `title`: Short human-readable title.
- `date`: Date of the agent run or receipt creation.
- `agent_type`: General type of agent, such as local coding agent or review assistant.
- `task_summary`: Plain summary of the requested work.
- `boundaries`: Array of explicit limits, such as local-only, no publishing, or no credentials.
- `changed_files`: Array of relative public-safe file paths or descriptions.
- `verification`: Array of commands or review steps that were actually run.
- `human_gate`: Object describing approval status and approval note.
- `public_action_taken`: Boolean indicating whether a public action happened.
- `notes`: Extra context, caveats, or follow-up needs.

## Human Gate

Use `pending` when approval is still needed. Use `approved` only when a human reviewer has explicitly approved the action. If `public_action_taken` is `true`, validation requires `human_gate.status` to be `approved` and `human_gate.approval_note` to contain text.

## Sharing Guidance

Before sharing a receipt, review every field for secrets, private paths, proprietary traces, and unnecessary operational detail. A short public-safe summary is usually better than a complete private record.

