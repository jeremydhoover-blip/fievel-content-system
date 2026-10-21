# Research round 3: visible systems, first use and bundled knowledge

Reviewed 2026-10-21. Scope: the user's added expectation of a viewing UI and stronger
experience/knowledge quality. These are primary-source design/tool references,
not evidence of Fievel user outcomes. No graph library was installed or tested.

| Question | Observation and source | Fievel inference / proposed action | What would validate it? |
|---|---|---|---|
| How should a system be represented? | [Backstage's system model](https://backstage.io/docs/features/software-catalog/system-model/) uses typed entities and explicit relationships to describe a system. Its domain is software infrastructure. | Adopt the idea of explicit domain entities and named relations; do not import Backstage or its ontology. Derive source→rule→check links from actual fields. | Designers can trace one real relationship; unmodeled relations are not invented. |
| Should a graph be the main UI? | [React Flow](https://reactflow.dev/learn) supports node/edge interaction and has [accessibility guidance](https://reactflow.dev/learn/advanced-use/accessibility). That provides capabilities, not evidence that a graph is appropriate for Fievel. | Start by comparing an overview-led and a connection-led design. Keep editing/freeform graph layout out of the first viewer experiment. | Observe next-step finding, source tracing and status comprehension with beginners/experts. |
| Which graph tooling might we reuse? | [React Flow license](https://github.com/xyflow/xyflow/blob/main/LICENSE) and [Cytoscape.js license](https://github.com/cytoscape/cytoscape.js/blob/master/LICENSE) identify MIT. Cytoscape documentation could not be retrieved reliably in this pass. | Both remain candidates; neither is an adopted dependency. Prefer normal DOM for a small read-only relationship trail unless a graph task justifies a library. | Separate pinned spikes, including keyboard/text equivalence and realistic size; inspect exact release/package licenses before incorporation. |
| How do we preserve accessible meaning? | [W3C complex-image guidance](https://www.w3.org/WAI/tutorials/images/complex/) addresses textual descriptions; [meaningful sequence](https://www.w3.org/WAI/WCAG22/Understanding/meaningful-sequence.html) addresses reading order. | A spatial map needs a meaningful linear equivalent; text labels and normal controls remain primary. | Keyboard, narrow view and screen-reader tasks; no conformance claim from a mockup. |
| What does useful progress look like? | GOV.UK's [multi-task pattern](https://design-system.service.gov.uk/patterns/complete-multiple-tasks/) makes tasks/order/status visible; [check answers](https://design-system.service.gov.uk/patterns/check-answers/) supports reviewing supplied information. These are service patterns. | Show actual saved decisions/next action and review proposed mappings before adopting them. Avoid an opaque health score or stage completion inferred from file presence. | A learner explains what is draft, missing, checked and awaiting a decision. |
| How should local learning content be organized? | [Diátaxis](https://diataxis.fr/) distinguishes explanation, reference, how-to and tutorial; its [tutorial guidance](https://diataxis.fr/tutorials/) emphasizes meaningful guided activity. | Route by current task and knowledge need; keep focused explanations beside the action instead of loading an entire encyclopedia. | Learners can carry out and explain a small task; experts skip lessons without losing quality. |

## Decisions proposed from this pass

1. A local companion viewer is now in scope, following the user's amendment. It
   serves comprehension and review while repository files remain authoritative.
2. First implementation experiment: a read-only generated snapshot, no hosting or
   mandatory framework. Refresh/freshness needs to be explicit. This is a proposal;
   no production renderer has been implemented.
3. Explore two UI priorities, overview-led and connections-led, using fictional
   example content. The conversation alternatives do not read the live repository.
4. Improve three bundled local modules that directly support standards integration,
   system relationships and instructions/skills. Route relevant workflows to them.
   These are draft authored lessons, not independently validated teaching material.
5. Keep educational knowledge, organizational standards and changing external tool
   documentation distinct. Routine covered explanations should use local material;
   current tool facts may still need verification.

## What we deliberately do not conclude

No evidence yet that a graph improves learning, that users prefer either UI, that
HTML snapshots are sufficient for every workflow, or that the expanded knowledge
library improves instruction adherence. Do not treat a curated module as company
policy or a source link as verified grounding. The viewer and knowledge tasks need
the acceptance experiments in ../experience/VIEWER-DESIGN.md and
../experience/KNOWLEDGE-ARCHITECTURE.md.

## Reuse boundaries

Reference the patterns, author Fievel-specific content, and preserve upstream
license distinctions. GOV.UK site guidance identifies OGL v3.0 where applicable;
no site code/content has been copied here. Diátaxis is referenced as an organizing
framework, not copied as a curriculum. No React Flow/Cytoscape source or assets
were incorporated. W3C explanatory material informs validation criteria; it is
not an accessibility certification for a proposed interface.
