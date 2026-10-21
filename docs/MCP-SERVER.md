# Fievel MCP servers

Fievel ships two MCP servers built on the same code ([ADR-008](decisions/ADR-008-mcp-servers.md)).

| | Local server | Hosted server |
| --- | --- | --- |
| Used by | Claude Code plugin (`.mcp.json`) | Codex plugin (`mcp.json`) |
| Runs | On the user's computer, over stdio | Google Cloud Run, over HTTPS |
| Files | Reads and writes new files inside the project only | Never sees files; works on content the agent sends |
| Tools | Setup status, init, validate, status, check, review, view, review page, review validation, source audit, consumer export, lessons, templates, format | Lessons, templates, format, validate package, check responses |
| Stores | Only the files you ask for, in your workspace | Nothing; content is not logged |

Run locally: `python scripts/mcp_local.py` (set FIEVEL_WORKSPACE to the project
root) or `PORT=8080 python scripts/mcp_remote.py`, then POST JSON-RPC to `/mcp`.

## Deploy the hosted server to Google Cloud Run

Use Cloud Shell, the browser terminal in the Google Cloud console; it already has
`gcloud`. Cloud Run needs a billing account even within the free tier; set a
budget alert in Billing.

1. In <https://console.cloud.google.com>, create or select a project, then open
   **Cloud Shell** (the terminal icon at the top right).
2. Get the code and deploy. Accept the prompts to enable APIs.
   ```sh
   git clone https://github.com/jeremydhoover-blip/fievel-content-system.git
   cd fievel-content-system
   gcloud run deploy fievel-mcp --source . --region us-central1 --allow-unauthenticated --memory 256Mi --max-instances 3 --concurrency 20 --timeout 60
   ```
   `.gcloudignore` uploads only what the image needs. Note the service URL it
   prints, such as `https://fievel-mcp-abc123-uc.a.run.app`.
3. Check it: `curl https://<service-url>/healthz` should return the version.
4. Domain verification: when OpenAI's portal shows a challenge path and token,
   serve them and re-check in the portal:
   ```sh
   gcloud run services update fievel-mcp --region us-central1 --update-env-vars FIEVEL_CHALLENGE_PATH=<path>,FIEVEL_CHALLENGE_TOKEN=<token>
   ```
5. Put `https://<service-url>/mcp` in `plugin-src/remote-mcp.json`, rebuild the
   Codex bundle and ZIP, and run the tests.

To update after a change, repeat step 2 from an updated clone (`git pull`). With
`min-instances` left at 0 the service sleeps when idle; the first request after
idle takes a few seconds.
