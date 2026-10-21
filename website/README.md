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

## GitHub Pages

Live at <https://jeremydhoover-blip.github.io/fievel-content-system/>, published
from [jeremydhoover-blip/fievel-content-system](https://github.com/jeremydhoover-blip/fievel-content-system)
branch `main`. Pages uses **GitHub Actions** as its source.

To republish after changing `website/dist`, push to `main`, then run **Publish
landing page** from the Actions tab (or `gh workflow run pages.yml --ref main`)
and check the deployed URL.

The workflow uploads only `website/dist`, never the repo, local user packages,
research evidence or credentials. It has no push trigger, so pushing alone does not
publish. No custom domain or CNAME is configured; the site uses the project
subpath `/fievel-content-system/`.

Workflow design follows [GitHub's official Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

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


## Current content direction

The page explains Fievel and the content system it helps users set up. The graph
connects product context, standards, sources, AI behavior, instructions and skills,
evaluations and governance. The animated conversation introduces Fievel and guided
setup. Domain examples and internal file artifacts were rejected for this page.
See [the correction](../docs/experience/evidence/landing-page-03/RESULTS.md).


## Design guide

[Site design guide](DESIGN-GUIDE.md) records the palette, typography, writing
rules, components, motion behavior and proposed next color-depth pass.
