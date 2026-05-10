# ckn-bw — agent & contributor guide

## What this repo is

A [BundleWrap](https://bundlewrap.org/) configuration-management repo
for ~22 personal/family-infra nodes. Nodes, groups, and bundles are
defined in plain Python; `bw apply` deploys the resulting state to
real machines.

Note: the root `README.md` is the maintainer's personal scratchpad,
not project documentation. Onboarding lives **here**, in `AGENTS.md`.

## Quickstart for agents

Five rules; follow these and you won't break things:

1. **Read-only by default.** Never run `bw apply`, `bw run`, or
   `bw lock` without explicit user request — even with `-i`. Stick
   to `bw test`, `bw nodes`, `bw groups`, `bw bundles`,
   `bw items`, `bw metadata`, `bw hash`, `bw debug`. See
   [`docs/agents/commands.md`](docs/agents/commands.md) and the
   fork's [safety envelope](https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md).
2. **Never echo decrypted secrets.** Don't print, paste, or log the
   value behind a `!password_for:`, `!decrypt:`, or
   `!32_random_bytes_as_base64_for:` magic string — not even from
   `bw debug` exploration. See
   [`conventions.md#secrets`](docs/agents/conventions.md#secrets).
3. **Don't touch the do-not-modify list.** `.secrets.cfg*`, `.venv`,
   `.cache`, `.bw_debug_history`, `.envrc`, root `README.md`. Treat
   `hooks/` and `items/` (custom item types) with extra care: a
   broken hook or item type breaks every `bw` command repo-wide.
4. **Use the fork.** The venv runs editable from
   [`github.com/CroneKorkN/bundlewrap`](https://github.com/CroneKorkN/bundlewrap)
   (branch `main`). Behavior tracks upstream `main`; the fork's
   [`AGENTS.md`](https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md)
   is the canonical bundlewrap-language reference. See
   [`conventions.md#bundlewrap-version`](docs/agents/conventions.md#bundlewrap-version).
5. **Prefer adding helpers to `libs/`** over duplicating logic across
   bundles. Repo-wide helpers go in
   [`libs/`](libs/AGENTS.md), reachable as `repo.libs.<x>`.

## Layout

| Dir | What's there |
|---|---|
| [`bundles/`](bundles/AGENTS.md)              | 103 bundles. One subdir per bundle (`items.py`, `metadata.py`, `files/`). |
| [`nodes/`](nodes/AGENTS.md)                  | One file per node (~22). `eval()`-loaded; demagified through `repo.vault`. |
| [`groups/`](groups/AGENTS.md)                | Group definitions, organized by axis (`applications/`, `locations/`, `machine/`, `os/`). |
| [`libs/`](libs/AGENTS.md)                    | Shared Python helpers reachable as `repo.libs.<modulename>`. |
| [`hooks/`](hooks/AGENTS.md)                  | bw lifecycle hooks (`apply_start`, `test`, `node_apply_start`, …). |
| [`data/`](data/AGENTS.md)                    | Out-of-bundle data assets (apt keys, grafana dashboards, …). |
| [`items/`](items/AGENTS.md)                  | Custom item types (currently `download:`). |
| [`bin/`](bin/AGENTS.md)                      | Operator scripts; not invoked by bundlewrap. |
| [`docs/agents/`](docs/agents/conventions.md) | Repo conventions and command deltas. |

## How nodes, groups, and bundles fit together

- A **node** (`nodes/<location>.<role>.py`) declares the groups it
  belongs to and any node-local bundles + metadata overrides.
- A **group** (`groups/<axis>/<x>.py`) attaches bundles and shared
  metadata to its members. Groups inherit via `supergroups`.
- A **bundle** (`bundles/<x>/`) is one chunk of configuration:
  `items.py` produces the items (files, services, packages),
  `metadata.py` declares `defaults` and `@metadata_reactor` functions
  that derive metadata from other metadata.
- The repo-root loaders (`nodes.py`, `groups.py`) walk these dirs and
  `eval()` each file. `nodes.py` additionally **demagifies** the
  result, resolving `!password_for:` etc. through `repo.vault`. See
  [`conventions.md#eval-loaded-node-and-group-files`](docs/agents/conventions.md#eval-loaded-node-and-group-files)
  for the constraints this places on editors.
- Metadata merges along: `all → location → os → machine →
  applications → node`.

## Conventions you must know

| Topic | Where |
|---|---|
| Bundlewrap-language reference (item types, dep keywords, reactors) | Fork's [`AGENTS.md`](https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md) — read first if new to bundlewrap |
| Vault / demagify magic strings                                     | [`conventions.md#secrets`](docs/agents/conventions.md#secrets) |
| Bundlewrap install (editable from the fork)                        | [`conventions.md#bundlewrap-version`](docs/agents/conventions.md#bundlewrap-version) |
| Group inheritance order, naming patterns                           | [`conventions.md#group-inheritance-order`](docs/agents/conventions.md#group-inheritance-order), [`#naming-conventions`](docs/agents/conventions.md#naming-conventions) |
| Repo-specific bw command deltas (apt keys, suspended nodes, vault echo) | [`commands.md`](docs/agents/commands.md) |
| Lib helpers                                                        | top-of-file docstrings in `libs/*.py` (`head -1 libs/*.py`) |
| Suspension idioms (`*.py_`, `_old/`, "for now")                    | [`conventions.md#suspension-and-soft-delete-idioms`](docs/agents/conventions.md#suspension-and-soft-delete-idioms) |

## Where to look for examples

When writing a new bundle, copy patterns from one that already does
the thing you need:

| Pattern                                  | Look at |
|---|---|
| Vault calls inside metadata reactors     | `bundles/dm-crypt/metadata.py` (compact, focused) |
| Mako-templated files                     | `bundles/bind/items.py` (DNS zonefile rendering) |
| Cross-bundle reactor writing             | `bundles/nextcloud/metadata.py` (writes into `apt.packages`, `archive.paths`) |
| Custom `download:` items                 | `bundles/minecraft/items.py` |
| Node file (single-purpose)               | `nodes/home.server.py` |
| Group with `supergroups` chain           | `groups/os/debian-13.py` |

## Where this doc lives

- This file: `AGENTS.md` at the repo root.
- `CLAUDE.md` is a symlink to this file — both names point to the same
  content so different tools can find it.
- The personal TODO scratchpad (`README.md`) is **separate** and not
  project documentation.
