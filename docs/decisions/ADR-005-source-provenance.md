# ADR 005 Offline source provenance audit

Date: 2026-10-21
Scope: SRC-01 / SYS-01; no model calls or external access

Add a read-only sources-audit command. Preserve the seven-file package schema.
Accept optional explicit --provenance JSON holding rule/source evidence locators,
excerpts and declared conflicts. No implicit ingestion, source file reads or URL
fetches. Evidence remains user-supplied and unverified against the original.

Require --as-of YYYY-MM-DD for reproducible date checks. A freshness window is
optional via --max-age-days; do not invent organizational expiry policy. Invalid
or future review dates and broken evidence references are errors. Unknown owners,
review dates, permissions, unsourced rules, missing evidence locators and open
conflicts are warnings, not proof of policy inaccuracy. Flag approved-source
metadata as declared authority rather than authenticated approval.

Default exit 0 allows a structurally sound draft with warnings. Exit 1 means
findings contain errors, or warnings when --strict was selected. Malformed inputs
exit 2. Report finding counts and explicit limitations, never an overall content
approval. Optional --out uses exclusive creation and refuses overwrites.

Record conflicts only when supplied. Resolved records need a decision, owner and
date; reporting does not establish that the decision is correct. No semantic
contradiction detection, automatic rule approval, human review validation or live
source availability check is implied. Unknown original dates/owners stay null.
