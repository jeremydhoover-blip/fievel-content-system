# UI-03 — project-first hierarchy correction

2026-10-21. User rejected the green palette, decorative branding and confusing
page hierarchy. Removed the visible logo/wordmark, changed colors to neutral
light/dark tokens and typography to system sans, and moved navigation across the
top. Overview puts the saved next step before inventory and provides a real
continuation prompt rather than routing every next step to checks. Guides now
explain three optional tasks; Project health explains repair purpose and hides
raw JSON behind a technical disclosure with file-purpose descriptions. Each core
view explains what to inspect and where editing/execution happen.

Before assets are preserved here. 35 Python tests passed; seven browser fixtures
and 24 layout combinations passed with no observed script errors or unexpected
network requests. Browser tests now exercise continuation prompt, task-guide
selection and collapsed technical-file inspection. Screenshots and browser JSON
are included. These are technical checks, not user acceptance or an independent
accessibility review. The user-facing snapshot is overview-04.html; earlier
snapshots remain intact. No package content/schema was changed.
