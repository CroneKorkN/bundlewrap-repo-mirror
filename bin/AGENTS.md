# bin/

## What's here

Operator scripts — invoked manually by the maintainer, **not** by
bundlewrap itself. Each is a standalone Python (or shell) script that
opens the repo via `Repository(dirname(dirname(realpath(__file__))))`.

Discovery is by `ls bin/` plus the `# purpose:` header line at the top
of each script:

```sh
head -2 bin/*
```

## Conventions

- **`# purpose:` header.** Every script under `bin/` starts with
  `#!/usr/bin/env python3` (or appropriate shebang), then a
  `# purpose: <one-line description>` comment. Baseline enforced by
  `grep -L '^# purpose' bin/*`.
- **Self-contained.** A script must work when run from anywhere — it
  resolves the repo via the script's own path, not `cwd`.
- **Read-only by default.** Most operator scripts query/print state
  (`passwords-for`, `wireguard-client-config`). Mutating scripts
  (`upgrade_and_restart_all`, `mikrotik-firmware-updater`,
  `sync_1password`) are the exception, not the rule, and prompt for
  confirmation.

## How to add a script

1. Start from [`bin/script_template`](script_template) — it carries
   the canonical shebang + `# purpose:` header + `Repository(...)`
   bootstrap.
2. Add the `# purpose:` line; lowercase, terse, include a `usage:`
   example if the script takes arguments.
3. `chmod +x bin/<name>`.
4. The script can reach helpers via `bw.libs.<x>` exactly like a
   bundle does.

## Pitfalls

- **`bin/` is not on `$PATH` by default.** Invoke as `bin/<name>` from
  the repo root, or via `direnv` if `.envrc` exposes it.
- **Mutating scripts can hit Tier-3 territory** (per the fork's
  safety envelope). Don't run `upgrade_and_restart_all`,
  `mikrotik-firmware-updater`, or anything that does `node.run(...)`
  without explicit user instruction. See the fork's
  [`AGENTS.md`](https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md)
  for the three-tier model.
- **Vault echo.** Scripts like `passwords-for` print decrypted values
  by design; that's allowed for the human at the terminal but *not*
  for the agent — never paste output into chat, ticket, or PR
  description.

## See also

- [`script_template`](script_template) — canonical starter.
- [`docs/agents/conventions.md`](../docs/agents/conventions.md) —
  vault rules.
- [`docs/agents/commands.md`](../docs/agents/commands.md) — read-only
  bw-command guidance.
