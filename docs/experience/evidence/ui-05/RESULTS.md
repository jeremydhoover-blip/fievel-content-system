# UI-05 — visual density and structure

2026-10-21. User requested more visualization and less reliance on eyebrow labels,
URLs and text blocks. Removed repeated page eyebrows. Added a category diagram
with actual source/content-rule/behavior-rule/check counts, connection bars with
explicit non-quality semantics, source-reference and check-method distributions,
source cards with prominent linked-rule counts and collapsed document location,
and a two-column checks grid. Overview connection rows collapse long check wording;
large packages initially show eight rows with a reveal-all action. Individual
rule navigation and text equivalents remain available. No workflow UI added.

35 Python tests passed before final compact-card adjustment. Final browser run:
seven fixtures, 16 responsive combinations; diagram node/count-bar assertions,
collapsed detail assertions and existing safe-rendering/navigation checks passed.
No observed errors or unexpected network requests. Evidence screenshots preserved.
No intended-user or independent accessibility acceptance is claimed.
