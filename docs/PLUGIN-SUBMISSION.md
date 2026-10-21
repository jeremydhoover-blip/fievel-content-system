# Plugin directory submission

Prepared 2026-10-21 for version 0.2.1. Submission is done by Jeremy from his own
accounts; nothing here has been submitted. Push `main` and republish Pages first,
so the privacy policy URL is live when reviewers open it.

## Shared listing values

| Field | Value |
| --- | --- |
| Name | `fievel` (display name Fievel Content System on Claude, Fievel on Codex) |
| Version | 0.2.1 |
| Short description | Build your content system |
| Description | Build and improve a portable content system with guided workflows and local quality checks. |
| Category | Productivity |
| Website | https://jeremydhoover-blip.github.io/fievel-content-system/ |
| Support | https://github.com/jeremydhoover-blip/fievel-content-system/issues |
| Privacy policy | https://jeremydhoover-blip.github.io/fievel-content-system/privacy.html |
| Documentation | https://github.com/jeremydhoover-blip/fievel-content-system#install-as-a-plugin |
| License | MIT |
| Icon | `assets/fievel-logo.png` (512 × 512 PNG) |

Release notes: Six guided skills for building a portable content system: getting
started, content standards, sources, AI behavior, evaluations and audits. Local
Python tools validate your files, run saved-response checks and generate a
read-only viewer. Your project stays in your own folder.

## Claude: Anthropic directory

Requires a paid claude.ai plan. Guide: https://claude.com/docs/plugins/submit;
checklist: https://claude.com/docs/plugins/pre-submission-checklist.

1. Open https://claude.ai/directory/manage → **Submit new** → **Plugin bundle**.
2. Source: repository `jeremydhoover-blip/fievel-content-system`, plugin path
   `plugins/fievel-claude`, branch `main`.
3. Validate. Listing details are read from `.claude-plugin/plugin.json`.
4. Answer data handling and compliance (draft answers below), then submit.

The first validation held the name for review (`NAME_CONFUSABLE`: "fievel" is
one letter from the connector "level"). The Claude manifest and catalog now set
`displayName` to "Fievel Content System"; `name` stays `fievel`, so install
commands and `fievel:` skill names are unchanged. The `documentationUrl`,
`privacyPolicyUrl`, `supportUrl` and `icon` warnings need no action.

Checked locally with Claude Code 2.1.304: `claude plugin validate --strict`
passes for the plugin and the catalog; an isolated install from GitHub lists six
skills. Checklist items verified by tests: README over 40 words, MIT license,
every file under 256 KiB, 66 files (limit 512), text and PNG only, no symlinks,
version raised from 0.1.0 (now 0.2.1 after the live-trial fixes). Anthropic's security scan and human review are not run.

## Codex: OpenAI plugin directory

Requires identity verification for your OpenAI organization. Guide:
https://developers.openai.com/plugins/deploy/submission; desktop-only guide:
https://developers.openai.com/plugins/deploy/desktop-only.

1. Use the prepared `release/fievel-codex-0.2.1.zip` (ignored by Git), or rebuild
   it from the committed bundle so `plugin.json` sits at the archive root:
   `python -c "import shutil; shutil.make_archive('release/fievel-codex-0.2.1', 'zip', 'plugins/fievel')"`
2. In the OpenAI Platform, open Plugins → **Upload new or existing plugin**,
   choose your verified identity, choose **Skills only** and upload the ZIP.
3. Listing URLs and release notes are imported from `plugin.json`
   (`websiteURL`, `supportURL`, `privacyPolicyURL`, `publication.release_notes`).
   Terms of service is optional for skills-only plugins and is not set.
4. `requires_local_executor` marks Fievel **Desktop only**: it installs from the
   ChatGPT desktop app and runs in local threads. If the portal rejects that field,
   OpenAI says to contact a representative to confirm submission access.
5. Wait for the skill scan to pass, submit for review, then publish after approval.

Checked locally with Codex 0.162.0-alpha.17.2: the ZIP unpacks to the committed
bundle, installs as 0.2.1 in an isolated Codex home and exposes six `fievel:*`
skills. OpenAI's skill scan and review are not run.

## Draft data handling answers

Review before submitting; you attest to these.

- Reads or stores personal data: **Reads and stores.** Project files can hold names
  the user enters (content owners, source owners, reviewers) and anything in
  supplied sources. Everything stays in the user's folder; Fievel has no servers,
  accounts, analytics or telemetry. The privacy policy says so.
- Sends data to another service: **No.** The bundled Python tools and
  generated pages make no network requests. With the user's approval, setup
  installs `jsonschema` from the Python Package Index.
- Data retention: **Not retained.** Project files stay in the user's chosen
  folder; conversation handling belongs to the host agent.
- Intended for users under 18: **No.** The audience is professional content designers.
- Contact email: your choice.
