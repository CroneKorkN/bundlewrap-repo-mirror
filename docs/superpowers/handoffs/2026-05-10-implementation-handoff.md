# Handoff — implement agent-friendly docs for ckn-bw

Date written: 2026-05-10. Working directory for the next session:
`/Users/mwiegand/Projekte/ckn-bw`.

This handoff is self-contained. Read top-to-bottom. Source documents
referenced are tracked in this repo unless noted.

## Why this work exists

This BundleWrap config repo (`ckn-bw`, ~22 nodes / 103 bundles) had no
agent-facing orientation: no `CLAUDE.md` / `AGENTS.md`, only ~33 of 103
bundles have a `README`, and the root `README.md` is the maintainer's
personal TODO list. Agents landing cold spelunked through magic-string
secrets, eval()-loaded node files, vault helpers, lib helpers, and a custom
bundlewrap fork.

The work over the last few sessions was: brainstorm → spec → plan → fork
work (separate session) → user-story validation → Phase 0 prep → handoff
(this file). The next session implements Phase 1 (PR1 scaffolding) and
Phase 2 (seed bundle docs).

The maintainer is also using this work as design exploration for a future
agent-friendly config-management tool. Concrete bundlewrap-language
gotchas surfaced here (silent eval-load, magic strings, reactor
namespace-write side effects) inform that future tool's design.

## Where we are right now (commit checkpoint)

`git log --oneline` (4 commits ahead of origin/master, none pushed):

```
1da7097 README: drop stale 'install bw fork' instruction
3daf70d spec: incorporate fork pivot and bw-syntax corrections
b804350 add user-stories validation doc
7486c78 switch bundlewrap install to editable from CroneKorkN/bundlewrap@main
8ec99db add agent-friendliness design spec        ← prior session
```

Working tree at handoff:

```
?? .claude/                                              # local Claude settings, leave alone
?? bundles/left4dead2/files/scripts/overlays/test        # pre-existing, unrelated, leave alone
```

The venv runs **bundlewrap 5.0.3 editable** from
`https://github.com/CroneKorkN/bundlewrap.git@main`, cloned at
`.venv/src/bundlewrap/`. `bw test` passes through the (full-network)
sandbox.

## Source documents (read in this order)

1. **Spec** — `docs/superpowers/specs/2026-05-10-agent-friendliness-design.md`.
   Section §0 documents revisions; the rest describes target file shapes
   in detail. **Treat as source of truth for what each file must contain.**

2. **User-stories validation** —
   `docs/superpowers/specs/2026-05-10-user-stories-from-history.md`.
   21 stories grounded in 1169 commits of git history. Each story's
   "Implications for agent docs" section maps to specific content adds
   that the plan (below) records as "User-story validation findings."

3. **Implementation plan** —
   `~/.claude/plans/btw-are-you-sure-crystalline-balloon.md`. Contains the
   Approach (numbered steps), Workflow validation findings (7 content
   adds), User-story validation findings (16 content adds), seed list,
   and verification. **Read it.** Lives outside the repo because it was
   produced under Claude's plan-mode workflow.

4. **Fork's `AGENTS.md`** — at
   `https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md`. The
   canonical bundlewrap-language reference: safety envelope (3 tiers),
   after-change runbook, hash-diff workflow, dep-keyword cheat-sheet,
   metadata.py pitfalls. ckn-bw's docs link out to it instead of
   duplicating.

## Phase 0 — already done (don't redo)

✓ `requirements.txt` swapped from `bundlewrap ~=5.0, >=5.0.3` to the
editable github reference. Don't change back.

✓ User-stories doc added at `docs/superpowers/specs/2026-05-10-user-stories-from-history.md`.

✓ Spec corrected at `docs/superpowers/specs/2026-05-10-agent-friendliness-design.md`:
fork pivot, slim `commands.md` scope, bw-syntax corrections, seed-list
rebalance, and a new `§0. Revisions` log. Section numbering is unchanged
otherwise.

✓ Root `README.md` cleaned: stale "install bw fork" section removed.
Personal TODO above and the `# monitor timers` / `# git signing` blocks
below are untouched.

## Phase 0 — what's left

**Docstring/header pass on `libs/`, `hooks/`, `bin/`** — partially started
in this session, then reverted to a clean state at user request to land
this handoff. The next session does the whole pass cleanly.

Spec §5 corollary defines the rule: "Every `libs/*.py` and `hooks/*.py`
starts with a one-line module docstring. Every `bin/*` script starts with
a `# purpose:` header comment."

Files that need a docstring/header (verified absent at handoff time):

```
libs/  — 19 files: apt, bind, derive_string, grafana, hashable, hmac,
         ini, ip, local, nextcloud, nginx, postgres, rsa, ssh, systemd,
         tools, version, wireguard, wol  (all .py)
hooks/ —  5 files: known_hosts, skip_local_nodes, test_ptr_records,
         unique_node_ids, wake_on_lan  (all .py)
bin/   —  9 scripts: mikrotik-firmware-updater, passwords-for, rcon,
         script_template, sync_1password, timestamp_icloud_photos_for_nextcloud,
         upgrade_and_restart_all, wake, wireguard-client-config
```

For each: read the file, write a concise one-line description capturing
**what it's for**, not how it works. Place the docstring at the very top
of the file (after the shebang, if present), followed by a blank line,
then the existing first line. Example shapes:

```python
# libs/wireguard.py
"""wireguard: deterministic WireGuard private/public key + PSK derivation backed by repo.vault."""

import base64
...
```

```bash
# bin/wake
#!/usr/bin/env python3
# purpose: wake one node via WoL by name — usage: wake <node>.

from bundlewrap.repo import Repository
...
```

For files with `#!/usr/bin/env python` shebang in `libs/` (only
`derive_string.py` currently), put the docstring on the line immediately
after the shebang.

For files with a leading comment in `libs/` (only `rsa.py` has the
`# https://stackoverflow.com/a/18266970` link), place the docstring above
that comment so it's still the first statement.

Commit message style for this pass: `libs/hooks/bin: add one-line module
docstrings and # purpose: headers`. Single commit for the whole pass.

Use the file headers / function names / surrounding code to derive the
descriptions; don't trust git log alone — terse commit messages won't
explain a lib's purpose. The user-stories doc gives indirect signal for
some (`libs/version.py` was introduced for `bin/mikrotik-firmware-updater`,
etc.).

## Phase 1 — main scaffolding (PR1)

The core writing work, ~800–1000 lines total per the plan's scope estimate.

### Order

Per plan Approach:

1. `docs/agents/conventions.md`
2. `docs/agents/commands.md`
3. The 8 per-area `AGENTS.md` files (`bundles/`, `nodes/`, `groups/`,
   `libs/`, `hooks/`, `data/`, `items/`, `bin/`)
4. `bundles/AGENTS.template.md`
5. Root `AGENTS.md` (last so all link targets exist)
6. `ln -s AGENTS.md CLAUDE.md` (the symlink)

Each file's exact target content is in the spec (see paths above).
Augmentations beyond the spec are recorded in the plan as
"Workflow validation findings" (7 items) and "User-story validation
findings" (16 items). Examples of augmentations:

- `bundles/AGENTS.md` gets a "Before you start" header pointing at
  `conventions.md` as required reading (workflow validation §1).
- `nodes/AGENTS.md` gets the silent-eval-load pitfall (user-story §S2),
  the `*.py_` suspend convention (§S9), and the rename-failure-mode
  pitfall (§S19).
- `conventions.md` gets the suspension idiom ("for now / disable / dummy"
  — §S11), the iterative-commit context (§S4), the burst-state awareness
  (§S5), and the `_old` soft-delete pattern (§F6).
- Per-bundle template gets an optional `## Writes into` section for
  bundles whose reactors write cross-namespace (§S12).

**Read both validation-findings sections in the plan in full before
starting Phase 1.** They're scoped, file-keyed, and small individually,
but cumulatively they're the difference between "docs that look right" and
"docs that an agent can actually use."

### Style guardrails

- One balanced doc per audience boundary. The per-bundle `AGENTS.md`
  template (spec §3) is the canonical shape: prose at top, structured
  Python dict for metadata schema, optional sections only when useful.
- Mechanism over enumeration. Area docs say *how the area works*, not
  *what's currently in it*. Specifics live in self-describing files
  (per the docstring rule above).
- No editorializing. Don't write advice; write conventions.
- No comments unless they explain a non-obvious *why*. Same for prose:
  short, factual.
- Use the path conventions the spec uses (`docs/agents/...`, not
  `docs/agents/...md` repeatedly). Use full URLs to the fork
  (`https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md`) so
  links work in any rendered context.

### Verification before committing

Run all of these (some need network sandbox; sandbox is configured for
full-network access — see "Operating environment" below):

1. `bw test` — must pass (exit 0).
2. `bw nodes`, `bw groups`, `bw bundles` — repo loaders still work.
3. Internal-link integrity: `grep -oE '\]\([^)]+\.md[^)]*\)' AGENTS.md
   docs/agents/**/*.md bundles/AGENTS*.md` then `test -f` each path.
4. `readlink CLAUDE.md` resolves to `AGENTS.md`.
5. `grep -L '"""' libs/*.py hooks/*.py` reports zero files.
6. `grep -L '^# purpose' bin/*` reports zero non-binary scripts.
7. `git grep -i "bw fork\|bundlewrap-fork"` reports only legitimate
   fork-as-source references (no leftover stale install instructions).
8. **Workflow walk-through.** Trace the "implement a new bundle" path
   end-to-end against the written docs as if you were a fresh agent.
   Confirms the workflow-validation fixes actually closed the gaps.

## Phase 2 — seed bundle docs (PR2)

Ten bundles, each gets a `bundles/<x>/AGENTS.md` from the template.

| # | Bundle | Existing README? | Notes |
|---|---|---|---|
| 1 | `monitored` | check via `find bundles/<x> -name README.md` | meta-bundle, often misunderstood |
| 2 | `postgresql` | check | foundational |
| 3 | `wireguard` | check | own lib + bin script |
| 4 | `routeros-monitoring` | no | most-churned bundle (15 commits / 18mo) |
| 5 | `apt` | check | own lib |
| 6 | `nginx` | check | web foundational |
| 7 | `telegraf` | check | high cross-bundle ripple (writes into many namespaces) |
| 8 | `backup` | check | cross-node coordination |
| 9 | `letsencrypt` | check | cross-cutting |
| 10 | `nextcloud` | yes | complex, recent activity |

For each: derive the **Metadata** section by reading the bundle's
`metadata.py` *and* running `bw metadata <one-node-with-the-bundle>` to
confirm the resolved shape. Derive **Produces** from `items.py`. Derive
**Depends on** by checking what other bundles' artifacts (apt packages,
systemd services) the bundle's reactors and items reference — use
`ccc search` (cocoindex; index already built at `.cocoindex_code/`) for
cross-bundle lookups when filling this in.

Where a bundle has an existing `README.md`, fold its content into the new
`AGENTS.md` and remove the old `README.md` in the same commit. Do not
lose information — those READMEs are the only existing human-prose
description for those bundles.

For bundles whose reactors write into other bundles' namespaces (notably
`telegraf`, `monitored`, `archive`, `wol-waker`, `apt`, `nextcloud`),
fill in the optional `## Writes into` section.

About 23 other bundles also have a `README.md` (not on the seed list).
Those stay in tree, untouched, until Phase 3 leave-as-you-go folds them.
Document this transition state in `bundles/AGENTS.md` so an agent
reading both isn't confused.

## Phase 3 — leave-as-you-go convention

Not a code task. The rule lives in `bundles/AGENTS.md`: any time an agent
or the maintainer materially edits a bundle, top-up or create its
`AGENTS.md`. The remaining ~93 bundles are filled lazily as they're
touched.

## Decisions captured (do not relitigate)

- **Doc audience.** One balanced doc per artifact, serving both humans
  and agents. No separate `README.md` + `AGENTS.md` split per bundle.
- **Fork hosts bundlewrap-language docs.** Don't duplicate items / metadata
  semantics in ckn-bw. Link out.
- **Read-only by default.** Agents do not run `bw apply`, `bw run`, or
  `bw lock` autonomously. Never. Even with `-i`. The fork's AGENTS.md
  spells this out as Tier 3.
- **No tooling work in this scope.** No `bw` wrapper, no Makefile, no CI,
  no lint. The plan and spec both call this out as a non-goal.
- **Per-bundle metadata as Python dict** (not bullet list). Matches how
  `metadata.py` actually looks; trailing comments carry type / required /
  default.
- **Bundle naming**: lowercase-hyphenated (`bind-acme`, `routeros-monitoring`,
  `wol-waker`). Underscores were used in deleted `_old` bundles, none
  remain.
- **Node naming**: `<location>.<role>.py` (e.g. `home.server.py`, `htz.mails.py`).
- **`*.py_` suspend convention** is real and intentional — never delete.
- **Commit-message style**: lowercase, terse subject; multi-line body
  with bullets when relevant; `Co-Authored-By: Claude Opus 4.7 (1M context)
  <noreply@anthropic.com>` trailer when Claude assisted. Look at recent
  commits for tone.
- **Don't push without asking.** Local commits only unless the user
  explicitly says push.

## Pitfalls — things that bite

- **`bw hash` does NOT accept selectors.** Only literal node/group names.
  Selectors (`bundle:<x>`, `group:<x>`) work for `bw apply`, `bw run`,
  `bw nodes`, but `bw hash` is the exception. To scope to a bundle:
  `bw nodes bundle:<x>` to enumerate, then `bw hash <node>` per result.
- **`bw items <node> <id> -p` is wrong** — the flag doesn't exist. Use
  bare form for expected state, `--preview` (`-f`) for rendered file
  content, `--attrs` for internal attributes.
- **`bw groups -n <node>` doesn't exist** — use `bw nodes <node> -a groups`.
- **Sandbox + macOS `localhost` quirk.** If you hit `errno 47
  EAFNOSUPPORT` on a localhost-proxy connection, `/etc/hosts` may have
  collapsed `127.0.0.1 localhost` and `::1 localhost` onto malformed
  lines. Verify with `python3 -c "import socket;
  print(socket.getaddrinfo('localhost', 80, type=socket.SOCK_STREAM))"` —
  must include both `('127.0.0.1', 80)` and `('::1', 80, 0, 0)`. (This
  was already fixed in this session; documenting in case it regresses.)
- **`bw test` makes outbound HEAD requests** to verify download URLs.
  Sandbox needs `allowedDomains: ["*"]` (or equivalent) for it to pass.
  Fall back to `dangerouslyDisableSandbox: true` if sandbox network
  blocks unexpectedly.
- **Eval-loaded node files.** `nodes/*.py` and `groups/*.py` are
  `eval()`'d as Python expressions. No top-level imports allowed. A
  syntax error or import causes the loader to silently drop the node
  from `bw nodes` (vanilla bundlewrap behavior). The maintainer's
  `groups.py` was patched in `dc40295` to print errors — a real foot-gun
  to document in `nodes/AGENTS.md`.
- **Don't restore the 9 partially-edited libs from the prior session.**
  They were intentionally reverted to give the next session a clean
  starting point; redo from scratch using your own judgment + file
  contents.

## Operating environment

- **Working dir**: `/Users/mwiegand/Projekte/ckn-bw`.
- **venv path**: `.venv/`. `bundlewrap` is editable at `.venv/src/bundlewrap/`
  on branch `main`, currently at commit `42dabfc2`. To pull upstream changes:
  `(cd .venv/src/bundlewrap && git pull)`.
- **Sandbox**: enabled, `network.allowedDomains: ["*"]`, network passes
  after `/etc/hosts` was un-corrupted. `bw test` works under the sandbox.
- **ccc index** at `.cocoindex_code/` — already built (768 chunks, 340
  files). Use `ccc search "<query>"` for semantic codebase exploration.
  Particularly useful in Phase 2 for finding what consumes a given
  metadata key or imports a given lib.

## What is intentionally NOT in scope

Re-listing so the next session doesn't drift:

- No tooling: no Makefile, no `bw` wrapper, no lint, no CI, no
  pre-commit hooks.
- No code refactoring, renaming, or splitting bundles.
- No mass-fill of all 103 bundles' `AGENTS.md` up front. Phase 3 is
  leave-as-you-go.
- The root `README.md` (personal TODO) stays as-is now that the stale
  fork-install section is gone. Don't add a project-readme on top.
- No upstream contribution to bundlewrap (acknowledged future work, not
  this scope).
- No edits to the bundlewrap fork — that's a separate repo. The fork
  agent already shipped its `AGENTS.md`.

## Success criteria

Phase 0 docstring pass complete + Phase 1 scaffolding done + Phase 2 seed
bundle docs done. Verifiable by:

- `find . -name 'AGENTS.md' -not -path './.venv/*' -not -path './.git/*'`
  lists root, 8 area docs, the per-bundle template, and 10 seed bundle
  docs. (~20 files.)
- `readlink CLAUDE.md` → `AGENTS.md`.
- All internal links resolve (verification step 3 above).
- All `libs/*.py`, `hooks/*.py`, `bin/*` self-describe.
- `bw test` passes.
- A fresh agent can trace "implement a new bundle" through root → bundles
  → example → write → wire → verify, without spelunking.

## Quick start for the new session

If the new session has zero prior context:

```bash
cd /Users/mwiegand/Projekte/ckn-bw
git log --oneline -5                                      # see Phase 0 commits
cat docs/superpowers/handoffs/2026-05-10-implementation-handoff.md  # this file
cat docs/superpowers/specs/2026-05-10-agent-friendliness-design.md   # the spec
cat ~/.claude/plans/btw-are-you-sure-crystalline-balloon.md          # the plan
.venv/bin/bw test                                          # confirm baseline still green
```

Then start with the docstring pass (Phase 0 remainder), commit, then move
into Phase 1 file-by-file in the order listed above.
