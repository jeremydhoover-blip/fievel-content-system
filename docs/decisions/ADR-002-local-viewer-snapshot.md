# ADR-002: First real-file viewer is a read-only HTML snapshot

Date: 2026-10-21. Status: accepted for WP-09 implementation experiment.
Implementation: local generator and technical/browser acceptance completed;
intended-user and independent accessibility evidence remain pending.
User direction: proceed; selected design alternative Overview-led.
Related: UI-01–05, FR-10/11, EX-05/06, WP-09/10/11.

## Decision and boundaries

Add `python scripts/fievel.py view <folder> --out <new.html>` with optional
`--report <execution.json>`. Produce a standalone page with overview, actual saved
next action/open decisions, rule/source/check inspection, file contents and a
small bundled learning selection. Files remain authoritative. No editing, server,
automatic refresh, external assets or network requests. Existing paths are refused.
The first implementation uses normal HTML controls and a linear relationship
trail; no graph framework is needed for the current task. This is not a permanent
technology commitment or evidence of learner preference.

## Integrity and truthful evidence

The viewer is diagnostic: missing/malformed files and unknown/ambiguous references
must be visible. Core `validate` semantics remain unchanged. Schema-invalid sections
are excluded from typed presentation and labeled, rather than silently replaced
with valid-looking content. Declared links are not verified source grounding.
Read-only stored approval/stage labels do not prove their recorded events occurred.

No results load automatically. With an explicitly selected deterministic report,
compare package/response hashes and reproduce all literal outcomes using the
current engine. Present reproduced results as such; matching does not establish
response origin or overall quality. Mismatches/stale/unsupported reports must not
present trusted pass/fail totals. Completed human judgments are outside the current
validated contract and will not be represented as accepted review evidence.

The snapshot records generation time and input fingerprint/file digests. It cannot
detect later changes by itself. Browser reload only rereads that same snapshot;
regenerate to a new path to reflect new files. Clearly label the snapshot and this
limitation. Embedded response/project data may be confidential; the viewer makes
no upload, but sharing its HTML shares the embedded content.

## Rendering contract

Untrusted package/report strings are data. Escape JSON before embedding and render
text through DOM text nodes, not innerHTML. Source locations are displayed as
text, never executed or automatically fetched. A restrictive hash-based CSP allows
only the bundled script/style. Normal buttons/selects/details/headings support
keyboard and meaningful reading order; independent accessibility review is pending.

## Acceptance experiment

Generate real Wayfarer and partial/empty packages; inspect counts and declared
links. Surface missing/duplicate IDs, bad JSON, missing files and unsupported data.
Verify no source files change and an existing output is preserved. Supply matching,
stale and altered reports. Inject HTML/script strings and javascript: source URLs;
verify they remain inert text. Browser-check navigation, learning, rule selection,
report labels, keyboard flow, 320–1024px widths and unexpected network requests.
These tests establish local functionality, not learner outcomes or conformance.
