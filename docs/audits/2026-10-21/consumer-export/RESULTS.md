# Consumer export results

Date: 2026-10-21
Scope: SYS-02 / TR-10, ADR-006

Added export-consumer with a named consumer, explicit date, exclusive new output
and declared-approved default rule selection. --include-drafts explicitly exports
all rules for design review while preserving original status. Empty selections
are rejected. Context, source passages and instructions occupy separate fields;
no tool grant or automatic activation is inferred. Optional provenance preflight
rejects structural errors while preserving relevant warnings and conflicts.

Six new tests cover draft/approved selection, exact instructions/status/source IDs,
input preservation, hashes, data-only malicious source text, missing evidence,
broken references, conflicts, null configuration and overwrite refusal. Full suite:
78 tests passed. Eight adapters match. The real CLI generated example-draft.json
from the fictional example with five draft rules and explicit evidence excerpts.
That is an actual export, not a model response or approved consumer configuration.
No failing-first test evidence claimed in this increment.

No model calls, source fetching, native host installation or consumer execution.
Data separation tests do not establish AI injection resistance. Product context,
responsibilities and governance are marked unreviewed. Voice/terms/patterns lack
approval metadata and are not silently promoted into exported rules.

Next: offline clean-setup verification using locally available dependencies.
Owner composition, real consumer behavior, human rubric calibration and prepared
agent journey execution remain separate open gates.
