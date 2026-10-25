# Conventions

Repo-specific idioms an agent has to know before editing this BundleWrap
config. For bundlewrap-the-language reference (item types, dep keywords,
metadata-reactor semantics, after-change runbook), see the fork's
[`AGENTS.md`](https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md).

## Secrets

Secrets live in `.secrets.cfg` and are referenced from node files by
"demagify" magic strings. The loader (`nodes.py`) walks node dicts and
resolves any leaf string of the form `!<verb>:<arg>`.

| Magic string | Resolves to |
|---|---|
| `!password_for:<id>`                  | `repo.vault.password_for(id)` |
| `!decrypt:<ciphertext>`               | `repo.vault.decrypt(ciphertext)` |
| `!decrypt_file:<path>`                | `repo.vault.decrypt_file(path)` |
| `!32_random_bytes_as_base64_for:<id>` | `repo.vault.random_bytes_as_base64_for(id, length=32)` |

Magic strings are only resolved inside **node files** (everything under
`nodes/`). They are *not* resolved in group files, bundle metadata
defaults, or item attributes — call `repo.vault.<verb>(...)` directly
there.

**Never echo decrypted values.** Don't print, log, or paste them, even
in `bw debug` exploration. If you need a sanity check, hash or
fingerprint instead. This applies to AI agents and humans equally.

## Bundlewrap version

Bundlewrap is pinned to the `main` branch of the maintainer's fork
[`github.com/CroneKorkN/bundlewrap`](https://github.com/CroneKorkN/bundlewrap)
via `[tool.uv.sources]` in `pyproject.toml`:

```toml
[tool.uv.sources]
bundlewrap = { git = "https://github.com/CroneKorkN/bundlewrap.git", branch = "main" }
```

`uv sync` builds `.venv/` from `pyproject.toml` + `uv.lock`; direnv runs
it on entry where a `layout_uv` is defined, `uv run bw` syncs on its own. Non-editable — to pick up new fork commits,
re-run `uv sync --upgrade-package bundlewrap` and commit the updated
`uv.lock`. The fork's `main` tracks upstream `bundlewrap/bundlewrap` master;
the fork's [`AGENTS.md`](https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md)
is the canonical agent-oriented bundlewrap-language reference.

To hack on bundlewrap itself from inside this checkout, clone the fork
to a sibling path and override the source with an editable path dep —
not part of the default workflow.

## Eval-loaded node and group files

`nodes/*.py` and `groups/*.py` are loaded by `eval()` in `nodes.py` /
`groups.py` (top of the repo). Each file must be a single Python
expression — typically a dict literal.

Consequences:

- **No top-level imports.** No `from foo import bar`, no `import os`.
  Helpers go in `libs/` and are reached via `repo.libs.<x>` from
  bundle code, not from node files.
- **No statements.** No `if`/`for`/`def` at the top level. Use
  expressions (ternaries, comprehensions) instead.
- **A file that fails to eval aborts `bw`.** `groups.py` prints the
  failing file first (commit `dc40295`), `nodes.py` only the traceback.

## Group inheritance order

Supergroups merge before their subgroups, the node wins last; see
[`groups/README.md`](../../groups/README.md#inheritance-and-merge-order).

## Naming conventions

| Where | Convention | Example |
|---|---|---|
| `nodes/*.py`     | `<location>.<role>.py`               | `home.server.py`, `ovh.mails.py` |
| `groups/*.py`    | one file per group; subdir = purpose | `groups/applications/nextcloud.py`, `groups/os/debian-13.py` |
| `bundles/<name>` | lowercase, hyphen-separated          | `backup-server`, `bind-acme`, `routeros-monitoring` |
| Custom items     | `items/<type>.py`                    | `items/download.py` |

Bundle names use no underscores.

## Suspension markers

Commits or comments saying "for now", "disable", "dummy" or "offline"
mark deliberate suspensions, not bugs. Check `git log -- <file>` before
re-enabling; the maintainer reverses these when the underlying
condition resolves.

## Files agents must not modify

| Path | Why |
|---|---|
| `.secrets.cfg*`         | vault key material |
| `.venv/`                | uv-managed Python environment — uv owns rebuilds, don't hand-edit |
| `.cache/`               | bw runtime cache |
| `.bw_debug_history`     | shell history for `bw debug` |
| `/.cocoindex_code/`     | local code index, not in git |
| `README.md` (root)      | maintainer's personal TODO scratchpad — not project docs |

Treat `hooks/` and `items/` (custom item types) with extra care: they
affect `bw`'s behavior for the whole repo, not a single bundle.

## Working style

- **Iterative commits are normal.** The maintainer commits in small
  checkpoints (`+`, `fix`, `whitespace`, terse one-liners). Don't
  rebase WIP branches without asking. As an agent, prefer
  complete-feeling commits over mimicking the iterative style.
- **Burst-state awareness.** Before writing into a subsystem, run
  `git log --since='1 month ago' bundles/<x>` (or `nodes/<x>.py`).
  ≥10 recent commits means the subsystem is in flux; read the most
  recent diffs first — your assumptions about its metadata shape may
  already be stale.
- **Branch names.** PRs go through the self-hosted Forgejo. Branch
  names are lowercase snake_case, descriptive
  (`debian-13`, `htz.mails_debian_13_squash`, `l4d2_the_next`).

## Bundlewrap-version migration recipe

When the next bw major lands:

1. Read the upstream migration guide.
2. `git grep` for affected reactor / item patterns.
3. Rewrite each (one commit per pattern is fine — see Working style).
4. Bump the bundlewrap source in `pyproject.toml` (or `uv.lock` via
   `uv sync --upgrade-package bundlewrap`) last.

Pattern from commit `186d503` (bw 4 → 5).
