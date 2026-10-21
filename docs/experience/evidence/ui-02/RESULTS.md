# UI refinement evidence — 2026-10-21

The user accepted the functional first pass and requested better heuristics,
design and experience. See [the review](../../UI-HEURISTIC-REVIEW.md) for findings,
research and scope. Baseline assets and hashes are preserved in this directory.

Implemented UIH-01–07: stronger overview hierarchy; searchable/type-filtered rule
list and inspector; URL/history navigation; visible snapshot disclosure; clearer
status language; useful empty/filter recovery; consistent responsive surfaces and
typography. Sources can now be inspected independently and followed back to rules.

Validation: 35 Python tests passed. The optional Playwright/Edge runner passed
seven generated package fixtures and 24 view/width combinations. It exercised
search preservation, clear filters, large-list expansion, native keyboard selection,
source navigation, history/direct links, report states and unsafe text. The
[browser results](viewer-browser-results.json) record no observed page errors or
unexpected page network requests. This is automated browser evidence, not an
accessibility certification or observed designer study.

Screenshots: [overview](viewer-overview-wide.png),
[rules](viewer-connections-wide.png), [narrow](viewer-connections-narrow.png),
[dark](viewer-connections-dark.png). The generated fixtures use authored fictional
content; selected reports reproduce literal checks and do not prove overall quality.

Reproduce with `python -m unittest discover -s tests -q`,
`python tests/prepare_viewer_fixtures.py <new-directory>`, then
`node tests/browser_viewer.cjs <new-directory>` with Playwright and a local browser
configured as described by the runner. No runtime UI dependency was added.

Remaining: intended designers finding their next action, tracing rules/sources,
and interpreting check status; independent keyboard/screen-reader accessibility
review. No learner outcome is inferred from these technical checks.
