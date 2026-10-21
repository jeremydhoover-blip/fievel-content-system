# Build a system in seven stages

An AI content system connects what your product does, how it communicates, what it
knows, how it behaves, and how you check its quality. The coding agent provides
the conversation; Fievel provides workflows, files and local verification.

Choose a path: beginner (learn with Wayfarer or your own product), existing
guidelines (map approved evidence first), or AI experience (start with tasks and
behavior gaps). All paths use the same files. Experts can set explanations to brief
and fill several stages at once. There is no forced tutorial gate.

For every stage, explain the work and its purpose, ask for the next useful decision,
show what was created, and explain what comes next. Save changes and decisions
in the selected package, then update progress.json. Stages are pending, drafted,
or reviewed; only use reviewed after an actual review. Rule approval is separate.

| Stage | What and why | Decisions to make | Artifact | Next |
|---|---|---|---|---|
| 1. Understand your product | Describe the experience so rules serve real tasks | Who needs help, doing what, with which constraints? | product.json | Identify content standards |
| 2. Understand your content | Make communication expectations reusable | Voice, terminology, patterns, accessibility and localization | standards.json | Find the evidence behind rules |
| 3. Identify your sources | Establish what the AI can know and trust | Authority, owner, dates, permissions and permitted use | sources.json | Set behavior boundaries |
| 4. Design AI behavior | Decide when to explain, ask, act or hand off | Responsibility, clarification, confirmation, uncertainty, recovery | behavior.json | Define good behavior |
| 5. Define quality | Turn requirements into things people can check | Ordinary and difficult situations; literal or human methods | evaluation.json | Try saved responses |
| 6. Try and improve | Learn from real evidence | Run available checks, review meaning, propose changes | New execution report, human review and improvement note | Plan ownership |
| 7. Maintain your system | Keep rules useful after this session | Owner, review cadence, approval, version and change history | governance.json and updated progress.json | Resume with the next open decision |

Start with one product task, two or three content rules and behavior boundaries,
then create situations that cover them. Source IDs connect evidence to rules;
requirement_id connects rules to checks. Draft suggestions without evidence keep
source_ids empty. Do not fill gaps with plausible company policy.

During stages 1–4, `validate` checks structure and existing links while reporting
rules that still need quality checks. Those gaps do not make a draft corrupt.
Before running stage-6 checks, use `python scripts/fievel.py validate <folder> --require-coverage`
after creating the stage-5 definitions. The check/review commands
also enforce coverage. Neither validation mode approves the content or proves
that its quality checks are well designed.

To create a project, run `python scripts/fievel.py init my-content-system` in the
repository root. To practice with fictional material, add `--example`. The CLI
copies templates; the agent and designer supply real product decisions. Unknown
fields are explicit, not silently filled with fictitious facts.

To resume, say “Resume Fievel in my-content-system.” Read progress.json and relevant
artifacts, run `status` and `validate`, summarize saved decisions and continue the
next action. If files are malformed, explain the validation error and repair it
within the user's agreed scope before interpreting the system. Moving the entire
folder preserves progress across compatible tools.

After a useful saved step, Fievel can generate a local read-only viewer with
`python scripts/fievel.py view <folder> --out <new.html>`. Use Overview to see
the saved next action/decisions and Connections to inspect declared sources and
checks for a rule. Local lessons are included. The viewer also helps inspect a
broken or partial package, but it does not repair files or approve content.
It is a snapshot; regenerate with a new filename after editing. To inspect a
specific execution report, add `--report <execution.json>`; report reproduction is
distinct from overall quality or completed human review.

## Try saved responses

Copy actual response text into a JSON object mapping scenario IDs to strings.
Record separately where those responses came from (model/version, date and prompt,
or clearly identify them as authored examples). Commands do not contact an AI:

```sh
python scripts/fievel.py check my-content-system --responses examples/responses-good.json --out my-content-system/results/run-01.json
python scripts/fievel.py review my-content-system --responses examples/responses-good.json --out my-content-system/results/review-01.json
```

Use the fixture only with a Wayfarer project. It is authored teaching text, not
live model output. Human checks remain pending. A reviewer reads situation,
context, rule, source and response, then records reviewer identity, reviewed_at,
pass/fail and rationale in the human_review sheet. Fievel does not automate human
judgments. The opt-in evidence format supports record validation through
`validate-review`; see docs/HUMAN-REVIEW.md. Record validity does not authenticate
the reviewer or establish that their judgment is correct. Keep AI suggestions in a
separate note labeled as such. Make suggested changes reviewable before applying
them, record accepted decisions, and rerun to a fresh output file.

`contains` and `not_contains` use case-insensitive literal substrings, including
within longer words. They are deliberately small checks, not a terminology engine
or semantic evaluator. Passing them says nothing conclusive about truthfulness,
accessibility or authorized actions. The “good” fixture includes an unsupported
refund claim to demonstrate that limit. Missing situations remain not_run.
