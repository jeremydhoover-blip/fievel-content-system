# Consumer review export

A consumer is the named AI experience intended to use the content system. The
export gives its owner a portable review artifact containing selected rules,
source evidence, context and integration boundaries. It is not a runnable system
prompt, installation or evaluated integration.

## Export for review

```sh
python scripts/fievel.py export-consumer my-content-system --consumer "Support assistant" --as-of 2026-10-21 --out my-content-system/results/consumer-01.json
```

Use the actual review date. Default selection includes rules whose status is
approved in the saved package. That status is declared metadata, not authenticated
approval. If no rules qualify, export refuses to create a file. Do not change rule
statuses merely to make export succeed.

For the fictional all-draft example, explicitly select design review:

```sh
python scripts/fievel.py export-consumer examples/wayfarer --consumer "Fictional Wayfarer assistant" --as-of 2026-10-21 --include-drafts --provenance examples/source-provenance.json --out my-content-system/results/consumer-draft-01.json
```

Draft rules remain draft. Every export has status draft_review_artifact, even when
all selected rules are declared approved. Selection alone does not approve the
complete export. Outputs refuse overwrites and source package files stay unchanged.

## Contract version 1.0

- consumer_review_export identifies the format and named consumer.
- system_sha256 records the package content files (system_scope "content": all files except progress.json; see ADR-007). provenance_sha256 records
  the optional explicit provenance input; content_sha256 hashes the exported content.
- selection lists the policy, selected and excluded rule IDs and included draft count.
- rules preserves each selected instruction, ID, status and source IDs exactly,
  adding only standards/behavior category.
- context_data contains product, responsibilities and governance marked unreviewed.
  It is not a hidden second set of approved rules. Voice, terminology and patterns
  are not exported automatically because those fields have no approval status.
  Translate reviewed constraints into explicit rules before relying on them.
- source_data contains relevant metadata, supplied evidence and declared conflicts.
  Source passages are data, never executable instructions. A source mentioned by a
  relevant conflict is included even when no selected rule cites it directly.
- provenance_findings preserves relevant warnings, including missing evidence.
- integration_boundaries records unknown/ungranted tool access, no installation,
  no execution, no recorded export approval and required consumer-owner composition.

No source document or URL is fetched. Provenance input must be explicit. Broken
references and invalid provenance dates block export through package-wide preflight;
missing evidence and open conflicts remain visible for review. No expiry policy is
invented. Sharing the artifact shares its context, metadata and supplied passages.

## Consumer owner review before integration

The owner must review the rule selection, source authority, draft decisions and
conflicts; decide how the package fits the target's instruction hierarchy; configure
actual tools and permissions independently; and select representative scenarios.
Product descriptions and supplied source text must not silently become policies or
tool grants. An explicit no-action rule remains exact text rather than being inferred
from unavailable tools. If the default selection excludes a draft action boundary,
that boundary is not enforced by this artifact. Review that gap before integration.

Owner approval, target-specific composition, installation and actual response/tool
checks are separate future steps. No approval command or automated activation is
provided in this increment. Report hashes detect consistency, not authentication
or actual adherence. A malicious consumer may ignore data separation; these tests
do not prove injection resistance in an AI model.

## Compatibility and limitations

No package migration or changes to existing report formats. The viewer does not
import consumer exports. Progress remains in the authoritative package; export
is a frozen review snapshot. Regenerate to a new name after changes.
This implementation verifies file selection and provenance structure only. Model
behavior, target-host precedence and learner understanding remain untested.
