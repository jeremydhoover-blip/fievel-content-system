# Contributing to Fievel

Content designers can contribute lessons, fictional examples and better review
questions without building a model integration. Explain the user need and show a
small before/after example. Use invented data; never include company documents,
credentials or real customer conversations without appropriate rights.

Install Python 3.10+ dependencies as described in README.md. Run
`python -m unittest discover -s tests -v` and
`python scripts/fievel.py sync --check` before proposing a change.

The local viewer lives in scripts/viewer.py and viewer/. Its report checks and safe
rendering are part of the test suite. Optional browser QA can be reproduced with
tests/prepare_viewer_fixtures.py and tests/browser_viewer.cjs; setup and evidence are
in docs/experience/evidence/viewer-01/RESULTS.md. It requires test-only Playwright/
browser access, not a production runtime dependency. Keep untrusted strings as text
and never add external viewer requests or silently reinterpret evidence statuses.

Edit canonical skills in .agents/skills, then run `python scripts/fievel.py sync`.
Generated adapters are not independent implementations. Knowledge modules need
plain explanations, examples, common mistakes, exercises, related concepts, primary
references and a reviewed date. Add the reference to knowledge/sources.json; label
version-sensitive and experimental material accurately.

Schema changes need compatibility notes, representative invalid fixtures and a
migration plan for breaking changes. Evaluation changes need both passing and
failing cases. Do not equate schema validation with production quality or claim
platform compatibility without a recorded runtime test.

Third-party code requires a recorded license and preserved notices. Reference links
alone do not grant reuse rights. Contributions to original Fievel files use the
project's MIT license. User content systems keep their own rights and governance.
