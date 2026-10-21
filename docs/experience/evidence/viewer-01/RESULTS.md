# Viewer implementation experiment — I-03

Date: 2026-10-21. Target: overview-led local HTML snapshot generated from actual
package files. Decision: [ADR-002](../../../decisions/ADR-002-local-viewer-snapshot.md).
This is technical evidence, not learner validation or accessibility certification.

## Implemented

`python scripts/fievel.py view <folder> --out <new.html>` creates a standalone,
read-only overview with actual saved next action/decisions, recorded progress,
product context, content/behavior rules, declared sources and quality checks.
The connections view preserves scenario/context and file/record locators.
Three local lessons and safely presented JSON files/diagnostics are included.

The diagnostic reader reports missing files, JSON/schema errors, duplicate IDs,
missing/ambiguous links and uncovered rules. Invalid sections are excluded from
typed presentation. It does not inspect the physical availability/content of
source locations; a linked source record remains a declared relationship only.

Optional `--report` selects a deterministic report. Matching package identity,
response identity and reproduced outcomes are required before totals are displayed.
Stale/altered/unsupported reports get no current totals. Human questions remain
not run; completed human judgments and response origin are not verified.

The page embeds selected data and original bundled lessons, a generation timestamp,
file digests and package fingerprint. It contains no external assets, backend,
watcher or editing interface. Hash-based CSP and text-node rendering keep source
strings inert. Refresh requires generating a new file; browser reload is not sync.

## Tests

The [pre-implementation attempt](before-implementation.txt) could not import the
not-yet-created viewer module. The implementation then passed **35 automated
tests**, comprising 23 existing core tests and 12 viewer tests. A first assertion
mistakenly searched HTML-escaped CSP as raw text; it was corrected to inspect the
decoded attribute value. No CSP restriction was relaxed to satisfy the assertion.

Viewer coverage: real relationships/counts; empty/partial drafts; missing/ambiguous
source/requirement IDs; malformed/missing/schema-invalid sections; exclusive output;
unchanged inputs; script/HTML injection strings; report identity/outcome/timestamp
checks; unsupported reports; CLI execution from another working directory.

Browser QA: seven generated packages (normal, empty, broken, malformed, stale,
hostile and 185-rule larger package). Checked actual navigation, rule selection,
keyboard rule changes/focus, lessons, report/diagnostic states, 20 width/view
combinations at 1024/736/360/320px, and hostile strings including a special
`constructor` scenario ID. No script errors, CSP errors or unexpected page network
requests were observed. Wide/narrow/dark screenshots were inspected.
Exact browser version and outcomes are in browser-results.json.

## Reproduce

Core: `python -m unittest discover -s tests -v`.
Generate fixtures in a new directory:
`python tests/prepare_viewer_fixtures.py .scratch/viewer-browser-check`.

Optional browser QA needs Node, Playwright and an installed compatible browser:
`node tests/browser_viewer.cjs .scratch/viewer-browser-check`.
Set FIEVEL_PLAYWRIGHT_MODULE if Playwright is outside Node's normal module lookup;
set FIEVEL_BROWSER_EXECUTABLE to an installed browser path if the bundled browser
is unavailable. These are test-only dependencies; opening generated HTML needs
neither Node nor Playwright. No browser download is performed by the runner.
The default environment's sandboxed browser profile could not be created; the
successful run used installed Edge headlessly with a separate temporary profile
outside the sandbox. No personal browser session was accessed.

## Limits and next evidence

The viewer presents recorded stage/approval labels, not proof of those events.
It cannot detect changes after generation, identify every policy conflict or
reconstruct an old package from its hash. Large-package QA is a functional smoke
check, not a performance benchmark. Independent screen-reader/contrast and actual
designer-task evaluation remain pending. Next: observe finding the next action,
tracing one source/rule/check and explaining the difference between defined,
reproduced and human-reviewed evidence. Do not equate these passing tests with
the larger guided experience being accepted.
