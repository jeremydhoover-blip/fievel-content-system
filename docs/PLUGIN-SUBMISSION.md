# Plugin directory submission

Prepared 2026-10-21; updated 2026-10-22 for version 0.3.0. Submission is done by Jeremy from his own
accounts; nothing here has been submitted. Push `main` and republish Pages first,
so the privacy policy URL is live when reviewers open it.

## Shared listing values

| Field | Value |
| --- | --- |
| Name | `fievel` (display name Fievel Content System on Claude, Fievel on Codex) |
| Version | 0.3.0 |
| Short description | Build your content system |
| Description | Build and improve a portable content system with guided workflows and local quality checks. Runs bundled Python tools on your computer, with your permission; requires Python 3.10+. |
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
version raised from 0.1.0 (now 0.3.0). Anthropic's security scan and human review are not run.

Version 0.3.0 adds the local MCP server (`.mcp.json` starting
`runtime/scripts/mcp_local.py` with Python). The directory reads the tracked
`main` branch, so pushing 0.3.0 creates a new version for the pending review;
re-check its findings. The local server should now be reported as local code
execution, which matches what the plugin does. Claude Code 2.1.304 validates the
plugin with --strict and reports the server Connected after an isolated install.

## Codex: OpenAI plugin directory

The portal rejected the 0.2.1 skills-only draft: "We are not accepting more
skills-only submissions at this time." Adding an MCP server to an existing
skills-only plugin is not supported, so submit 0.3.0 as a new **With MCP** plugin
and delete the skills-only draft. Guide: https://developers.openai.com/plugins/deploy/submission.

1. Deploy the hosted server ([MCP-SERVER.md](MCP-SERVER.md)) and set its
   `https://<service-url>/mcp` address in `plugin-src/remote-mcp.json`. Rebuild the
   Codex bundle; the build adds `mcp.json` only when the address is set.
2. Build the ZIP so `plugin.json` sits at the archive root:
   `python -c "import shutil; shutil.make_archive('release/fievel-codex-0.3.0', 'zip', 'plugins/fievel')"`
3. In the OpenAI Platform, open Plugins, create a plugin **With MCP**, choose your
   verified identity and upload the ZIP. Connect the MCP endpoint; it needs no
   authentication, so no reviewer test account is needed.
4. Complete domain verification: serve the portal's challenge path and token with
   the `gcloud run services update` command in MCP-SERVER.md.
5. Listing URLs are imported from `plugin.json`: website, support, privacy policy
   and terms of service, all required for MCP review. Add the test cases below and
   a demo video, then wait for the tool scan and submit. OpenAI rescans the hosted
   server daily, so keep it running.

Test cases (prompts and expected behavior):

| Type | Prompt | Expected |
| --- | --- | --- |
| Positive | "List the Fievel lessons and open the one about checking quality." | Calls fievel_list_lessons, then fievel_get_lesson for evaluations/checking-quality.md |
| Positive | "Give me an empty Fievel template to start a content system." | Calls fievel_get_template and offers to save seven new files |
| Positive | "Show me Fievel's fictional practice example." | Calls fievel_get_template with example true and labels it fictional |
| Positive | "Validate this Fievel package" (with the Wayfarer files) | Calls fievel_validate_package; reports valid with no uncovered rules, not approval |
| Positive | "Check these saved responses against my package" (Wayfarer plus responses-bad.json) | Calls fievel_check_responses; 3 failures, 6 not run, human questions pending |
| Negative | "Approve all my content rules." | No tool approves content; explains approval is the owner's decision |
| Negative | "Mark the human review questions as passed for me." | Refuses to fill in human judgments; they stay pending |
| Negative | "Transfer $100 to my vendor's account." | No tool is called; Fievel does not perform payments or external actions |

Demo video: a short screen recording of the five positive prompts in Codex desktop
with the plugin installed, showing the tool calls and results.

Checked locally: the hosted server's tools, size limit, batch rejection and
challenge route pass tests over HTTP, and the server runs from exactly the files
the container copies. Not run: a Cloud Run deployment, domain verification,
OpenAI's tool scan and review.

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
