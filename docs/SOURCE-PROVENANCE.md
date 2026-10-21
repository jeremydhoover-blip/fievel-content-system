# Source provenance checks

Use sources-audit to inspect declared source metadata and evidence relationships
without ingesting sources or calling a model. It does not modify the project.

```sh
python scripts/fievel.py sources-audit examples/wayfarer --as-of 2026-10-21
python scripts/fievel.py sources-audit examples/wayfarer --as-of 2026-10-21 --provenance examples/source-provenance.json --max-age-days 365 --strict --out my-content-system/results/provenance-01.json
```

Use the actual audit date. The example 365-day window is an explicit demonstration,
not Fievel policy. Omit --max-age-days when no review interval has been decided;
then no source is labeled expired based on age. --out refuses existing files.

## Meaning of findings

Missing owners, review dates, permissions and evidence locators are warnings.
Unsourced rules can be legitimate early drafts and are also warnings. An old
review date warns only against the supplied age window. Invalid or future dates,
unknown rule/source references, evidence from an undeclared rule source and duplicate
locators are errors. Declared approved authority generates a warning because this
command cannot authenticate approval. Dates and ownership are not filled in for you.

Default exit 0 allows drafts with warnings; exit 1 indicates errors. --strict also
returns 1 for warnings. Invalid input structure or IO errors return 2. Zero findings
means only that these declared metadata checks found no issue, not that content is
correct, approved, current or ready to publish.

## Explicit provenance input

The optional file has version 1.0, evidence and conflicts arrays. It does not change
the seven-file content-system schema. The examples/source-provenance.json fixture
contains actual copied passages from the fictional handbook. These are illustrative
mappings, not reviewed organizational standards. Do not infer unrecorded conflicts
from an empty conflicts array.

Each evidence record has rule_id, source_id, locator and excerpt. The source ID must
exist in sources.json and be declared in that rule's source_ids. Locator and excerpt
must be nonempty. Multiple passages can cite the same rule/source with different
locators. Neither the locator nor passage is checked against the original file.
The command never opens source locations or URLs. It also does not check whether
an excerpt semantically supports the rule. That needs source review.

Each declared conflict has id, source_ids (at least two unique IDs), description,
status (open or resolved), resolution, decided_by and decided_on. Unknown decision
fields stay null. Open conflicts warn. Resolved conflicts require nonempty decision
text, owner and a valid date no later than the audit date. This verifies the record,
not the authority or correctness of the resolution. There is no automatic conflict
resolution or semantic contradiction detector.

Source permissions and declared ingestion are metadata. Unknown permissions warn,
including when ingestion is marked true. They do not authorize reading, copying or
sharing. Obtain the owner's permission separately. Locators, excerpts and metadata
can be sensitive; keep confidential material outside tracked files.

## Reproducibility and next review

Reports record package/configuration hashes, audit date, supplied age threshold,
findings and limitations. Re-run against current files before reusing findings.
The report does not approve source content or enforce permissions. Human review
should inspect exact passages, declared authority, permitted use and unresolved
conflicts before promoting a draft rule to an approved standard.
