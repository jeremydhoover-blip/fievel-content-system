# ADR 008 Local and remote MCP servers

Date: 2026-10-22
Scope: Codex directory submission; LT-03 command friction; plugin distribution

OpenAI's plugin portal now rejects new skills-only submissions ("We are not
accepting more skills-only submissions at this time"), and local MCP plugins are
limited to approved partners. A public Codex listing therefore needs a remote MCP
server at a stable public HTTPS endpoint. Separately, the live Claude trial showed
shell commands cause avoidable permission prompts.

Decision: one dependency-free MCP implementation (`mcp_protocol.py`) with shared
read-only knowledge tools (`mcp_tools.py`) and two servers.

- `mcp_local.py`, stdio, shipped in the Claude bundle through `.mcp.json`. It wraps
  the CLI: init, validate, status, check, review, view, review page, review
  validation, source audit and consumer export, plus setup status and lessons.
  Every path resolves inside FIEVEL_WORKSPACE (the project root); outputs are new
  files only. It finds jsonschema in the workspace's `.fievel-venv`. No network.
- `mcp_remote.py`, Streamable HTTP with JSON responses, hosted on Google Cloud Run
  and referenced by the Codex bundle's `mcp.json`. Stateless and read-only:
  lessons, templates, the package format, package validation and literal checks
  on content the agent sends. No storage, accounts or content logging; requests
  are capped at 2 MiB and batch requests are rejected. An optional plain-text
  route serves the directory's domain-verification token.

Skills prefer these tools and fall back to the CLI. The privacy policy and terms
describe the hosted server; the Claude plugin never uses it. The Codex manifest
keeps `requires_local_executor` because its skills still run the local CLI for
project files; this is revisited if the portal rejects the combination.

Not chosen: the MCP Python SDK (adds dependencies to a privacy-sensitive local
tool), a hosted server that stores projects (accounts, retention and security
burden), and adding the remote server to Claude (it would require a separate
connector submission and gives Claude Code users nothing the local server lacks).
Origin checks against DNS rebinding matter for local HTTP servers; the local
server uses stdio and the remote one holds no state or credentials.
