# UI-04 — visualization-only scope correction

2026-10-21. User clarified the viewer is a dashboard visualization of content
created in their agent, not a workflow, onboarding or learning interface.
Removed continuation prompts, next actions, decisions-to-make, stage progress,
and all lesson navigation/rendering. Overview now shows recorded product context
and actual source → rule → check relationships; selecting a rule opens its
inspector. Four main views: Overview, Rules & connections, Sources, Checks &
results. Technical diagnostics remain a secondary route for unreadable data,
not a primary dashboard tab. Original project files are unchanged.

35 Python tests passed. Seven browser fixtures and 16 view/width combinations
passed, with no observed errors or unexpected network requests. Assertions cover
absence of workflow UI, actual relationship rows and rule selection. Screenshots
and machine results are preserved here. User acceptance remains pending.
