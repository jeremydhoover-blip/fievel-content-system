# Turn existing guidelines into a content system

Reviewed: 2026-10-21. Original draft Fievel teaching material. Independent domain
review and learner validation are pending. Type: task procedure with explanation.

## Learn and do

Use when a team already has writing standards, product policies or examples.
By the end, you should be able to turn one real standard into a traceable rule,
identify what the source does not establish, and choose a check that fits it.
You can follow the procedure without reading the explanation if you know these concepts.

## A guideline is evidence, not a complete AI instruction set

A style guide may explain voice, word choices and writing conventions. An AI
experience also needs context: which task it helps with, what information it has,
when to clarify, what actions it may take, and what to do when information is missing.
Do not invent these extra decisions merely to make the guide look complete.

Start with one authorized local file and one user task. Record the source's title,
location, owner if known, date if known, authority, permitted use and whether it has
actually been read/ingested. A file's presence or “approved” filename is not proof
of current organizational authority. Ask about consequential ambiguity instead of
silently resolving it. Inventorying the source does not automatically authorize
copying it into a public repository.

## Work in small mappings

For each candidate rule, identify the exact section or line, what it explicitly
says, its context, and what interpretation you are proposing. Keep a permitted
short excerpt or precise locator in a review note if the schema cannot yet store it.
Preserve meaning before improving phrasing. Separate requirements from examples,
suggestions and descriptions of current practice.

| Source statement | What it establishes | Proposed representation | What it does not establish |
|---|---|---|---|
| “Use member rather than customer.” | A naming convention in its stated scope | Content rule with source ID and locator; record approval as supplied | All future plural/localized forms; who the assistant may contact |
| “Keep messages calm.” | A tone direction | Draft operational examples and a human-review rubric | One objectively correct tone score |
| “You can usually renew a book.” | An uncertain general description | Open question until eligibility/conditions are established | A guaranteed renewal right, limit or tool permission |

The examples are fictional. Do not use them as actual library policy.

## Add behavior without inventing authority

If the guideline says nothing about acting, the next useful decision is about
responsibility and actual tools. A tone rule does not authorize issuing refunds,
renewing books or sending messages. Proposed behavior remains draft until the
relevant owner decides. A rule can cite a real source and still include an
unsupported interpretation; the link is not a certificate of grounding.

When sources conflict, identify both claims, dates, scope and authority. Sometimes
the newer source wins; sometimes a product-specific policy overrides general
guidance. Do not assume recency always establishes priority. If you cannot resolve
the conflict from authorized evidence, record the decision needed.

## Choose a check for what can go wrong

Exact wording can use a literal check when the wording itself is required. Meaning,
tone, fabricated policy and appropriate next steps need a rubric and contextual
review. A term search can miss inflections or flag part of an unrelated word.
Actual tool use requires tool evidence; “I completed it” in a response is not proof.

Save the new rule, source reference, related check and unresolved decisions. Default
validation accepts structurally valid drafts before checks are finished. Use strict
coverage before execution; do not call covered requirements passed requirements.

## Common mistake

Turning “use simple language” into “all responses must be fewer than 20 words”
without a source or owner decision. The numeric rule might obstruct a useful answer.
Show it as a proposal, explain its tradeoff and review it rather than claiming it
is the team's existing approved standard.

## Practice and check your understanding

Use the fictional guidelines in
../../evals/fievel-behavior/fixtures/library-guidelines.md. Map its first rule into a
structured standard, then propose how to handle a request to renew a book.

A sound answer preserves “member”, records the actual source/locator, distinguishes
the supplied terminology approval from a new behavior proposal, and leaves renewal
eligibility/tool access unknown. If your answer creates a renewal limit, you have
added unsupported policy. Explain why a literal terminology check would not catch that.

Related: [system relationships](system-relationships.md),
[instructions and skills](../ai-fundamentals/instructions-and-skills.md),
[checking quality](../evaluations/checking-quality.md).

Primary references: [GOV.UK patterns](https://design-system.service.gov.uk/patterns/)
for context-specific reusable guidance;
[Microsoft method selection](https://github.com/microsoft/ai-agent-eval-scenario-library/blob/04fc731937cd2bb8b9ef5195540c6f53914f52a5/resources/evaluation-method-selection-guide.md)
for selecting checks. The workflow above is Fievel's adaptation, not a claim that
these sources prescribe an organizational approval process.
