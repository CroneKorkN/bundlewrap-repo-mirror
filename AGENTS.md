# ckn-bw

BundleWrap configuration for personal and family infrastructure; `bw apply` deploys it to real
machines. The root `README.md` is the maintainer's scratchpad, not documentation.

## Rules

- Never run `bw apply`, `bw run` or `bw lock` unless the user asked for that run, interactive
  mode included.
- Never print a secret: no value behind a vault magic string such as `!password_for:`, `bw debug`
  included, and no config file on a node in full or with context lines, only the keys needed.
- Never edit `.secrets.cfg*`.
- Run `bw test` after touching `hooks/` or `items/`: a broken hook or item type breaks every
  `bw` command.
- Run bw as `uv run bw`: it is the fork pinned in `pyproject.toml`, and agent shells do not
  load direnv.

## Where to look

- The fork's [AGENTS.md](https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md) is the
  reference for the bundlewrap language.
- Read a directory's README.md before changing files there.
- Repo conventions are in `docs/agents/conventions.md`, repo-specific `bw` behaviour in
  `docs/agents/commands.md`.
- Shared helpers live in `libs/`, reachable as `repo.libs.<module>`, each described in its
  first docstring line.
