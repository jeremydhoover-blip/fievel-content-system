# ADR 006 Consumer review export

Date: 2026-10-21
Scope: SYS-02 and TR-10; offline only

Add export-consumer for an explicitly named consumer and new output path. Export
is a versioned review artifact, not an installation, deployment or evaluated agent.
Select declared-approved rules by default. --include-drafts is an explicit design
review option; preserve their draft status. Reject empty rule selections. Never
promote or relabel rules during export. Declared approval is not authenticated.

Separate selected rule text from unreviewed product context, responsibilities and
source evidence. Context and source passages are data, not executable instructions
or additional policy. Preserve the exact rule text, IDs, statuses and source IDs.
Include only selected evidence and relevant declared conflicts with their source
metadata. A rule status does not approve the complete export or grant tools.

Use the optional provenance file only when explicitly supplied. Validate reference
integrity through the existing provenance checker. Preserve missing evidence and
open conflict warnings; do not silently fill them in. No source file/URL fetching.
Record input hashes and an export content hash, consumer name, selection policy,
selected and excluded rule IDs, draft counts and explicit unknown tool capability.
No API key, model call, automatic consumer activation or enforcement claim.

Consumer owners must decide composition, higher-priority instructions, conflicts,
tool access, policy approval and evaluation in the actual target. A portable review
artifact cannot establish a platform's instruction precedence or actual behavior.
The initial contract deliberately stops before emitting a runnable system prompt.
No seven-file package migration or legacy-report change is required.
