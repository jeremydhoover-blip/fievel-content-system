# ADR 007 Content-scoped system fingerprint

Date: 2026-10-21
Scope: finding LT-01 from the live Claude Code trial; offline only

Every report recorded `system_sha256` over all seven package files, including
`progress.json`. Progress is session bookkeeping: decisions, open questions,
stage status and next action. AGENTS.md tells the agent to save it after each
meaningful step, so every check report, review sheet and viewer comparison went
stale as soon as the agent did what it was told. In the live trial one turn
produced three report versions and four overviews before cleanup.

Decision: identify a package by its content files only. `system_fingerprint`
hashes product, standards, sources, behavior, evaluation and governance, and
excludes progress. Governance stays in scope because ownership and change history
are part of the system a report describes. New reports record `system_sha256`
with `"system_scope": "content"`. Review evidence moves to version 1.1, whose
`system_sha256` uses the content scope; its snapshot still embeds progress for
context, but progress is no longer part of the identity hash.

Migration: no stored report is rewritten. A report without `system_scope`, and
review evidence version 1.0, keep the legacy meaning: a hash of all seven files.
`matches_system` compares each report using the scope it declares, so legacy
reports stay valid against an unchanged package and stale against a changed
one, exactly as before. Existing evidence under docs/audits and evals needs no
change. Consumer exports and source audits record the content scope as well;
neither compares hashes against a folder.

Consequences: editing progress no longer invalidates results; editing any rule,
source, situation, check or governance record still does. A report cannot detect
a changed next_action, which is intended. Tools reading `system_sha256` must read
`system_scope` first; an unknown scope is rejected rather than guessed.
