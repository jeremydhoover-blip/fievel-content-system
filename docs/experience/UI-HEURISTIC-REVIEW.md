# UI refinement: heuristic review and acceptance plan

Reviewed 2026-10-21. The user accepts the first functional UI pass and requests
improvement of heuristics, design and experience. This is the implementation
agent's review, not independent expert review or an intended-user study.
Baseline: overview-02.html and I-03 viewer assets, preserved under evidence/ui-02.

## Findings and bounded changes

| ID | Observed friction | Principle and proposed change | Check |
|---|---|---|---|
| UIH-01 | Audience, tasks, counts, decisions and seven stages compete in a long overview | Hierarchy/minimalism: saved next action first, compact clickable artifact summaries, open questions visible, supporting context/progress disclosed | Find next action and navigate from a real summary; detail remains accessible |
| UIH-02 | Long native rule labels provide little recognition or orientation | Recognition/efficiency: searchable rule list, type filter, selected state, readable rule detail; retain compact jump selector | Search by wording/ID, clear filters, inspect another rule; 185-rule fixture remains navigable |
| UIH-03 | Navigation has no history/deep links; headings/focus provide weak orientation | User control/status: view and selected rule in URL fragment, browser back/forward, clear current navigation and keyboard focus | Open a specific rule link, navigate back/forward, keyboard search/select |
| UIH-04 | Raw timestamp and snapshot explanation are buried after the page contents | Visibility: compact snapshot status in header, human-readable UTC timestamp and adjacent explanation | Recognize saved snapshot and locate regeneration instructions without reading a long footer |
| UIH-05 | Repeated defensive language and raw statuses interrupt every rule | User language/progressive disclosure: concise status labels; once-per-view evidence explanation; source/technical detail in native disclosures | No loss of caveats or false approval/result implication; stale/no-report states readable |
| UIH-06 | File errors and empty screens describe absence more than recovery | Recovery/help: explain next local action and expose matching diagnostics; distinguish empty package from zero search matches | Empty, broken, malformed and filtered states have useful routes; no fake edit/refresh action |
| UIH-07 | Styling lacks a consistent hierarchy between navigation, work area and metadata | Consistency/visual hierarchy: stronger typography, spacing/surface system, compact semantic badges and responsive workspace | Wide/narrow/light/dark inspection; focus, readable wrapping and no content overlap |

## Evidence informing this pass

[NN/G's usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
inform the review categories; they are rules of thumb rather than measured proof.
[GOV.UK summary lists](https://design-system.service.gov.uk/components/summary-list/)
inform readable label/value presentation. [W3C disclosure guidance](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/)
informs access to supporting detail using keyboard-operable disclosure controls.
These references do not dictate Fievel's visual style. No upstream implementation
or assets are copied. The proposed changes are local hypotheses to validate.

## Scope and validation

Keep the read-only snapshot contract, safe rendering, report reproduction and
source files unchanged. Improve the actual viewer rather than create a new mockup.
No editing, hosted service, telemetry or dependency addition. No invented health,
progress or quality score. Do not treat a saved stage label as observed learning.

Run existing Python safety/report tests and expand browser checks for search,
filters, selection, source navigation, deep links/history, disclosures, keyboard
focus and responsive layout. Preserve before/after screenshots and results. Then
test with designers: find the next action, find a particular rule, identify its
source/check and explain whether a result exists. Technical success does not close
the independent accessibility or intended-user evidence gates.
