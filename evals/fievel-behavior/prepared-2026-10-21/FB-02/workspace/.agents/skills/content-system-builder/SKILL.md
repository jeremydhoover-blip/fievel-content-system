---
name: content-system-builder
description: Build or improve portable Fievel content standards and product context using user decisions and approved sources.
---

# Content System Builder

Read AGENTS.md, docs/WORKFLOW.md and the selected project's progress.json.
Required inputs: selected project folder, product/audience intent, and any supplied
standards. Start with stages 1 and 2; ask only for missing decisions. Use the
existing-guidelines path to map supplied rules, preserving their source IDs and
approval status. Do not turn inferred preferences into approved organization rules.

For existing material, read knowledge/content-design/using-existing-guidelines.md.
Show a small source-to-proposed-rule mapping with precise evidence location where
available. Preserve meaning and distinguish explicit requirements from examples or
interpretation. Where the schema lacks a locator, keep a scoped review note rather
than invent fields or call a source ID verified evidence. Missing policy stays unknown.

Read knowledge/content-design/content-systems.md for beginner explanations only.
Create product.json and standards.json using templates/content-system as the shape.
Use stable rule IDs. Draft recommendations have status draft and empty source_ids
unless grounded in a recorded source. Collect accessibility/localization needs;
leave unknowns in progress.open_questions. Introduce a reusable language pattern
with an example. Continue through sources, behavior, quality, and governance via
docs/WORKFLOW.md; this skill can coordinate the complete seven-stage workflow.

Output: changed package files, saved decisions and next_action. Run
`python scripts/fievel.py validate <folder>` to check structure/links and show
uncovered draft rules. Do not force stage-5 checks into earlier stages merely to
make a draft valid. At stage 5, give every rule a linked scenario/check, then run
`python scripts/fievel.py validate <folder> --require-coverage` before execution.
Structural validity and coverage are not content approval or completion.
When useful, generate a read-only overview with
`python scripts/fievel.py view <folder> --out <new.html>` and explain the changed
rule's declared source/check connections. Regenerate to a new file after edits;
the prior snapshot does not update itself. Missing evidence remains a visible gap.
Summarize significant changes before editing; request approval before overwriting
user-owned assets outside the agreed editing scope. On validation failure, explain
the specific file/link and repair only the agreed project.
Example: “Use calm language” -> draft rule -> human tone-review question.
