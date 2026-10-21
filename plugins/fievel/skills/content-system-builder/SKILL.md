---
name: content-system-builder
description: Build or improve portable Fievel content standards and product context using user decisions and approved sources.
---

# Content System Builder

## Using this skill from the Fievel plugin

This plugin carries Fievel's workflows and Python tools. The user's project is
separate from the installed plugin. Find the plugin root two directories above
this SKILL.md; its `runtime/` directory is the bundled resource root, called R below.
Resolve R from this skill's actual installed path, never a development checkout.

- Read `R/AGENTS.md` for Fievel's conversation and workflow rules. References in
  this skill and in AGENTS.md to AGENTS.md, docs/, knowledge/, templates/, examples/,
  schemas/, scripts/ and .agents/skills/ are relative to R, not the user's working directory.
- Keep the current working directory in the user's chosen workspace. Run the CLI
  by its absolute path: `python "R/scripts/fievel.py" <command> <project> ...`.
  Replace R with the resolved path. Resolve project and output paths in the user's
  workspace. Never create projects, install dependencies, or edit inside R or the
  plugin cache. Never copy Fievel AGENTS.md over a user's repository instructions.
- Check Python 3.10+ and `python -c "import jsonschema"`. If missing, explain the
  prerequisite. When setup is authorized, create a new `.fievel-venv` in the user's
  workspace and install `R/requirements.txt` with its Python. Reuse a working
  environment; do not overwrite an existing environment. Use that interpreter for
  every CLI command. Do not install globally or claim the plugin bundles Python.
- Follow existing workspace instructions. Explain that project files remain local,
  but material read into the conversation is handled by the user's coding agent.
- The repository-maintenance and adapter-sync instructions in R/AGENTS.md are for
  Fievel development, not for modifying the installed plugin during a user session.
- Other Fievel skills in this plugin: getting-started, content-system-builder,
  source-discovery, ai-behavior-designer, evaluation-designer and content-audit.
  Switch to the one that fits when the user's request changes.

Save projects under the user's chosen folder (default `my-content-system/` in
their workspace). The user approves content; validation does not. Do not run
model evaluations unless the user authorized them.

## Workflow

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
