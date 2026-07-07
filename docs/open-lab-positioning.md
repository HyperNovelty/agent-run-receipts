# Open Lab Positioning

`agent-run-receipts` provides a small accountability primitive for the Hypernovelty Open Lab public footprint: a receipt for what an agent was asked to do, which boundaries applied, what changed, what verification ran, and whether a human gate remains.

It pairs naturally with:

- `ai-workflow-safety-screen` for deciding whether an AI-assisted workflow should require review before use.
- `source-card-schema` for evidence and provenance records.
- `hypernovelty-survival-kit` as the umbrella map for the six public proof repos.
- `hypernovelty-verification-literacy-kit` for teaching verification and recovery habits.
- `ai-school-readiness-kit` for education-specific readiness review.

## Public-Safe Boundary

Receipts are not private traces, legal records, compliance certifications, or authorization systems. A public receipt should use relative file names, synthetic examples, and concise summaries that do not expose credentials, account data, private paths, unpublished material, or proprietary internals.
