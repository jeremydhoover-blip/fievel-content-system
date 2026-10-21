# Fievel

**Your AI content systems architect.** Learn to build AI content systems by building one.

Fievel is a repository-native guide for content designers, UX writers, conversation
designers and AI experience designers. Work with a coding agent to connect product
context, writing standards, sources, AI behavior, quality checks and governance.
Your output is a set of readable, reusable files that you own.

This is the first functional prototype (0.1.0). It includes a seven-stage workflow,
six skills, draft templates, a complete fictional booking support example, and a
local command-line tool. There is no hosted service or custom agent framework.

The guided experience remains under validation. The current
[development plan](docs/DEVELOPMENT-PLAN.md) connects the original brief to
[requirements](docs/REQUIREMENTS.md), [audit findings](docs/audits/2026-10-21/REVIEW.md),
research, bounded changes and acceptance gates. [ITERATIONS.md](docs/ITERATIONS.md)
records what actually changed and which outcomes remain untested.

The intended experience now includes a local companion UI for viewing your system
and its connections, alongside the guided conversation and bundled learning material.
See [experience direction](docs/experience/EXPERIENCE-DIRECTION.md),
[viewer proposal](docs/experience/VIEWER-DESIGN.md) and
[knowledge architecture](docs/experience/KNOWLEDGE-ARCHITECTURE.md). UI alternatives
are design studies; a live/generated file viewer is not implemented yet.

## Start with your coding agent

1. Fork or clone this repository and open its root folder in your coding agent.
2. Ask: **“Read AGENTS.md and start Fievel. I'm new to AI content systems.”**
3. Choose fictional practice, bring existing guidelines, or describe your AI experience.
4. Let the agent help you create your files and choose the next useful decision.

No separate paid API key or MCP connection is needed for the fictional exercise.
Access to your chosen coding agent is separate and may require an account or plan.
Regular ChatGPT chat does not imply repository execution or skill discovery.

Codex uses AGENTS.md and canonical `.agents/skills/`. After opening a fresh session,
you can try `$getting-started`. Claude Code has generated `.claude/skills/` copies
and CLAUDE.md; try `/getting-started` after trusting the workspace. VS Code's coding
agent has `.github/copilot-instructions.md` and can read the canonical skills.
If discovery fails, use the explicit “Read AGENTS.md…” prompt above.
See [compatibility evidence](docs/COMPATIBILITY.md): automatic discovery and live
conversations in fresh agent sessions have not been tested.

The current session's skill catalog lists all six Fievel skills. That is limited
metadata-discovery evidence; it does not establish invocation, adherence or usability.

## Run the local exercise

Install Python 3.10+ with pip. In a terminal in this folder:

```sh
python -m pip install --target .deps -r requirements.txt
python scripts/fievel.py init my-content-system --example
python scripts/fievel.py status my-content-system
python scripts/fievel.py validate my-content-system
python scripts/fievel.py check my-content-system --responses examples/responses-good.json --out my-content-system/results/run-01.json
python scripts/fievel.py review my-content-system --responses examples/responses-good.json --out my-content-system/results/review-01.json
```

On macOS/Linux, use `python3` if `python` is unavailable. Dependencies install in
this folder; Fievel never installs global skills or changes editor settings. A
virtual environment with `pip install -r requirements.txt` also works.

The saved responses are authored fixtures. The first report has three literal
passes and six questions not run because they require human review. It does not
prove the assistant is good: the fixture deliberately includes an invented refund
time that only meaning-based review catches. Try `examples/responses-bad.json`
with a new output filename to see the three deliberate literal failures.

For your own product, omit `--example`, then describe the product to Fievel.
Templates have explicit unknowns. The CLI creates files; your coding agent guides
the conversation and helps populate them. It does not independently generate rules.

Draft rules can exist before their checks: default `validate` and `status` report
missing coverage while allowing staged work. Use `validate <folder> --require-coverage`
to require every rule to have a check. `check` and `review`
enforce that coverage automatically. This changes the prototype's earlier default
validation behavior; scripts relying on coverage failure should add the flag.

## What you create

| File | Purpose |
|---|---|
| product.json | Product, audience, tasks, constraints, accessibility and localization |
| standards.json | Voice, terms, reusable patterns and draft/approved rules |
| sources.json | Source authority, provenance, freshness and permissions |
| behavior.json | Responsibilities and action/communication boundaries |
| evaluation.json | Realistic situations and checks linked to requirements |
| governance.json | Owner, version, review process and change history |
| progress.json | Saved path, decisions, open questions and next step |

`my-content-system/` is ignored by Git by default. Review privacy before explicitly
sharing it. Initialization refuses existing folders. Reports refuse existing paths.
To resume, say **“Resume Fievel in my-content-system.”**

## What works today

Schema and relationship validation, saved progress, deterministic checks on saved
responses, pending human review sheets, six modular skills and synchronized adapters.
The full walkthrough is in [WORKFLOW.md](docs/WORKFLOW.md). See the
[Wayfarer example](examples/wayfarer/START-HERE.md) and [test evidence](docs/VALIDATION.md).

Promptfoo and Vale were researched but are not integrated. There is no live model
runner, LLM judge, external source ingestion or MCP connector. The educational
library is introductory. Human approval and completed judgments are not enforced
by the CLI. Structural validation does not establish source accuracy or completeness.

## Develop and contribute

```sh
python -m unittest discover -s tests -v
python scripts/fievel.py sync --check
```

Edit skills in `.agents/skills/`, then run `python scripts/fievel.py sync` to update
generated Claude copies. Read [CONTRIBUTING.md](CONTRIBUTING.md),
[architecture](docs/ARCHITECTURE.md), [research](docs/RESEARCH.md) and
[roadmap](docs/ROADMAP.md). Fievel code, original teaching text and examples are MIT
licensed; this license does not grant rights to user-provided organizational content.

Troubleshooting: if validation cannot import jsonschema, rerun the dependency
installation with the same Python executable. If a folder/report already exists,
resume it or choose a new path. Validation errors identify a field or broken ID.
Do not fix missing sources by inventing them. If your agent ignores instructions,
ask it to read AGENTS.md and the selected skill explicitly.
