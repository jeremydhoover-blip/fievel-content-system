# Fievel landing page

Buildless public page in `dist/`. Edit HTML/CSS/JS directly; no dependencies or
generated build step. The chat is an explicitly labeled fictional animated example,
not a recording, live agent or verified transcript. It uses controlled HTML
animation with typing dots, pause/resume/replay, a transcript and static
reduced-motion/no-JS fallbacks. Assets are code-native and
local; the page loads no third-party fonts, analytics or services.

## Local preview

From the repository root:

```sh
python -m http.server 8765 --bind 127.0.0.1 --directory website/dist
```

Open `http://127.0.0.1:8765/`. `dist/index.html` also opens directly as a local
file. Clipboard denial selects the text for manual copying. The site uses only
relative asset paths, so project Pages subpaths work without rewriting URLs.

## GitHub Pages, when ready

The user supplied repository is
[jeremydhoover-blip/fievel-content-system](https://github.com/jeremydhoover-blip/fievel-content-system).
The site uses that exact URL and its HTTPS clone command. Documentation/license
links assume the public branch is `main`; verify them after the initial push.
The repository was described as newly created; linked project content will only
exist after it is pushed. No push or deployment was performed here.

1. Push the project to that repository and confirm the public/default branch.
2. In repository Settings → Pages, select **GitHub Actions** as the source.
3. Run **Publish landing page** manually from Actions on the intended branch.
4. Verify links and assets on the returned deployed URL.

The workflow uploads only `website/dist`, never the repo, local user packages,
research evidence or credentials. It has no push trigger: creating these files
does not publish anything. No custom domain or CNAME is configured. Standard
project Pages would use the repository subpath `/fievel-content-system/`.

Workflow design follows [GitHub's official Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
Hosting availability/settings and successful remote execution are unverified.

## Validation

Optional local Playwright runner: `node tests/browser_landing.cjs`, with
`FIEVEL_PLAYWRIGHT_MODULE` and `FIEVEL_BROWSER_EXECUTABLE` if needed. Supply
`FIEVEL_LANDING_URL` to test a served project subpath instead of the local file.
Evidence is written to `.scratch/landing-page-02-qa/` by default.
Use `FIEVEL_LANDING_OUT` for a separate evidence directory. Existing core checks remain
`python -m unittest discover -s tests -q` and adapter drift checking.


## Revision plan

The user confirmed [the revision plan](../docs/experience/LANDING-PAGE-REVISION-02.md)
and it is implemented locally. Page writing has no eyebrow text, no punctuation
in titles and no em dashes. The revised page includes a concrete relationship
map, controlled animated chat and distinct section interactions. See
[revision evidence](../docs/experience/evidence/landing-page-02/RESULTS.md).
User review remains open; nothing has been pushed or published.


## Current content direction

The page explains Fievel and the content system it helps users set up. The graph
connects product context, standards, sources, AI behavior, instructions and skills,
evaluations and governance. The animated conversation introduces Fievel and guided
setup. Domain examples and internal file artifacts were rejected for this page.
See [the correction](../docs/experience/evidence/landing-page-03/RESULTS.md).


## Design guide

[Site design guide](DESIGN-GUIDE.md) records the palette, typography, writing
rules, components, motion behavior and proposed next color-depth pass.
