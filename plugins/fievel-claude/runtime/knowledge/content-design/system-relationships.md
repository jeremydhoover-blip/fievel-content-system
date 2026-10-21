# Understand the connections in your system

Reviewed: 2026-10-21. Original draft Fievel explanation. Independent review and
learner validation are pending. Intended for someone inspecting their first package.

## Learning objective

Explain the difference between a source link, a rule, a defined check and an actual
judgment. Use that distinction to inspect one relationship and identify what is missing.

A content system is more useful when its parts have clear relationships. A rule
can point to the document that informed it. A quality check points to the rule it
is meant to test. A situation explains when that check matters. A result records
what happened when a check actually ran against a response.

| Part | Question it answers | Current Fievel representation |
|---|---|---|
| Product context | Who are we helping, doing what? | product.json |
| Source | What information are we using, and with what authority? | sources.json |
| Rule | What communication or behavior is expected? | standards.rules or behavior.rules |
| Situation and check | When could this go wrong, and what would we inspect? | evaluation.scenarios and checks |
| Result/judgment | What evidence was actually assessed, by what method? | Separate execution report or human review |
| Decision and next action | What did we decide and what remains open? | progress.json and governance.json |

## Read a trail

In Wayfarer, source wayfarer-handbook is linked from behavior-1, which says not to
invent payment causes or refund dates. The payment-unknown situation has a human
question linked to that rule. The relationship helps you find what to review.
It does not establish that the rule faithfully represents the source or that the
response follows it. Someone must inspect the evidence and apply an appropriate check.

Technical terms: a stable **ID** names an item; a **reference** links to an ID;
**traceability** means you can follow a requirement through its evidence and checks;
**coverage** means a check has been defined for a requirement. Coverage is not quality.

## Use relationships to consider a change

Suppose the booking policy changes. Find rules citing that policy, then scenarios
checking those rules. Review whether their expected behavior or evidence needs
changing, and rerun relevant checks against new responses. These are declared
dependencies to inspect, not proof of every possible effect. Rules with no source
link may also be relevant; the system does not know what was never recorded.

If a response report uses a different system fingerprint, it may be stale. A hash
can identify a difference but cannot explain it or reconstruct an older package
by itself. Keep old versions/evidence when reproducibility matters.

## Common mistakes

“Connected” does not mean approved. “Checked” may mean only a phrase search.
“Reviewed” needs actual reviewer evidence, not a stage label. A missing source link
is a gap to inspect, not proof a draft rule is wrong. A visually neat graph can
hide all of these differences if its labels are unclear.

## Practice and check your understanding

Open examples/wayfarer/evaluation.json from the repository root. Follow
no-refund-promise to its requirement and source. Then inspect the refund response
in examples/responses-good.json. Why can its literal run have no failures while
the response is still unacceptable?

A sound explanation identifies the unsupported 48-hour claim, observes that
the relevant human question has not run, and distinguishes literal results from
the source-bound judgment still needed. You should not describe that fixture as
a good assistant merely because its filename says “good”.

Related: [using existing guidelines](using-existing-guidelines.md),
[checking quality](../evaluations/checking-quality.md).
References: [Backstage system model](https://backstage.io/docs/features/software-catalog/system-model/)
as an example of typed system relationships; [Promptfoo assertions](https://www.promptfoo.dev/docs/configuration/expected-outputs/)
for different check methods. Fievel's relationships above describe its current
files, not the Backstage ontology or a Promptfoo integration.
