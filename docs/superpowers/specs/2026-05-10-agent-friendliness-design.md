# Agent-friendly repo — design

Date: 2026-05-10

## 1. Goals & non-goals

**Goal.** Make this BundleWrap config repo legible to agents (and humans) so an
agent can land useful work — adding/modifying a bundle, configuring a node,
running read-only `bw` introspection, doing a cross-cutting refactor — without
spelunking and without unsafe side effects.

**In scope.**

- Root entry point: `AGENTS.md` (with `CLAUDE.md` as a symlink to it).
- Per-area `AGENTS.md` for `bundles/`, `nodes/`, `groups/`, `libs/`, `hooks/`,
  `data/`, `items/`, `bin/`. Mechanism-focused; no enumeration of contents.
- Per-bundle `AGENTS.md`: one balanced doc per bundle, replacing existing
  bundle `README.md` files. Template provided.
- `docs/agents/conventions.md`: repo-specific idioms (vault magic strings,
  custom bundlewrap fork, files-not-to-touch).
- `docs/agents/commands.md`: read-only `bw` command allowlist and an
  after-change runbook keyed by what was edited.
- `docs/agents/bundlewrap/`: a focused folder explaining bundlewrap-as-used-here.
  Three files at first: `README.md`, `items.md`, `metadata.md`.
- A docstring/header pass on `libs/*.py`, `hooks/*.py`, `bin/*` so each
  individual file self-describes.
- Phase 2 seed: per-bundle `AGENTS.md` for 10 bundles selected empirically.

**Out of scope (explicitly).**

- No tooling changes: no `bw` wrapper, no Makefile, no lint, no CI.
- No code refactoring, renaming, or splitting bundles.
- No mass-fill of all 103 bundles' `AGENTS.md` up front. Phase 3 is leave-as-you-go.
- The root `README.md` (personal TODO list) stays untouched.
- Contributing `AGENTS.md` upstream to bundlewrap is acknowledged but out of
  scope for this work.

## 2. Information architecture

```
ckn-bw/
├── AGENTS.md                       # root entry point (agents + humans)
├── CLAUDE.md                       # → symlink to AGENTS.md
├── README.md                       # untouched (personal TODO)
├── docs/
│   └── agents/
│       ├── conventions.md
│       ├── commands.md
│       └── bundlewrap/
│           ├── README.md
│           ├── items.md
│           └── metadata.md
├── bundles/
│   ├── AGENTS.md                   # what bundles are, how they compose
│   ├── AGENTS.template.md          # template for per-bundle docs
│   └── <bundle>/
│       └── AGENTS.md               # per-bundle doc (replaces existing READMEs)
├── nodes/
│   └── AGENTS.md
├── groups/
│   └── AGENTS.md
├── libs/        AGENTS.md
├── hooks/       AGENTS.md
├── data/        AGENTS.md
├── items/       AGENTS.md
└── bin/         AGENTS.md
```

**Reading order an agent should follow.** Root `AGENTS.md` → relevant area
`AGENTS.md` → specific `bundles/<x>/AGENTS.md` → `docs/agents/conventions.md`
or `docs/agents/bundlewrap/<file>` only when something non-obvious comes up.

**Per-area files (not just root).** An agent editing `bundles/nextcloud/items.py`
already has `bundles/AGENTS.md` and `bundles/nextcloud/AGENTS.md` adjacent in
the file tree. Locality of reference matters more than centralization.

**Existing per-bundle `README.md` files (~10 of them).** Folded into the new
`AGENTS.md` and removed in the same change, so there is exactly one doc per
bundle.

## 3. Per-bundle `AGENTS.md` template

One balanced doc serving both audiences. Prose where prose helps, structure
where structure helps. Sections in order:

````markdown
# <bundle-name>

<1–3 sentences: what this bundle does and when you'd use it.>

## Usage

<How to apply: which group(s) typically include it, or how a node opts in.
Minimal example of node metadata if any keys are required.>

## Metadata

Keys read from `node.metadata`:

```python
{
    'nextcloud': {
        'domain': 'nc.example.com',   # str, required — public hostname
        'admin_user': 'admin',        # str, default 'admin'
        'apps': [],                   # list[str], default [] — apps to enable
        'preview': {
            'enabled': True,          # bool, default True
        },
    },
}
```

## Produces

<Brief list of items created: files, services, packages, users, etc.
One line each. Skip if trivially obvious from items.py.>

## Depends on

<Other bundles required, or "none". Note ordering quirks if any.>

## Gotchas

<Non-obvious behavior, manual steps, known pitfalls. Omit the section if none.>
````

**Design choices.**

- Free-form prose at the top (purpose, usage) keeps it readable for humans skimming.
- Metadata is a Python dict literal — matches how `metadata.py` actually looks,
  shows nested structure at a glance. Trailing comment per leaf carries type,
  required/default, and a short note.
- `Produces` and `Gotchas` are optional — skip when there is nothing useful to say.
- No version/changelog/author fields — git already covers that.

## 4. Root `AGENTS.md` content

Target ~150 lines. Sections in order:

1. **What this repo is.** 2–3 sentences. BundleWrap config-management for
   personal/family infra (~22 nodes), Python-defined nodes/groups/bundles,
   applies to real machines.
2. **Quickstart for agents.** Five bullets, the operating envelope:
   - Default to read-only `bw` commands; never `bw apply`/`bw run`/`bw lock`
     without explicit user request. See `docs/agents/commands.md`.
   - Never paste/echo decrypted secret values; respect the demagify magic-string
     convention. See `docs/agents/conventions.md`.
   - Do not modify `.secrets.cfg*`, `.venv`, `.cache`, `.bw_debug_history`,
     `.envrc`. Everything else is editable, but treat `hooks/` and `items/`
     (custom item types) with extra care — they affect bw's behavior or item
     resolution across the whole repo.
   - Uses a custom **bundlewrap fork**, not upstream — check
     `docs/agents/conventions.md` before assuming upstream behavior.
   - Prefer adding helpers to `libs/` over duplicating logic across bundles.
3. **Layout map.** Terse, link-rich. One line per top-level dir, each linking
   to that area's `AGENTS.md`.
4. **How nodes/groups/bundles fit together.** 5–10 lines: nodes pick up bundles
   via groups; metadata flows from groups → node → metadata processors;
   `nodes.py` and `groups.py` (root) are the loaders that walk the dirs and
   run `demagify`.
5. **Conventions you must know.** One-line summary + link for each:
   - `docs/agents/bundlewrap/README.md` — read first if new to bundlewrap.
     `items.md` and `metadata.md` are deep dives for the hard parts.
   - `docs/agents/conventions.md#secrets` — secrets / demagify magic strings.
   - `docs/agents/conventions.md#fork` — custom bundlewrap fork.
   - `docs/agents/conventions.md#groups` — group inheritance order.
   - `docs/agents/commands.md` — safe `bw` commands and after-change checks.
   - Lib helpers — see top-of-file docstrings in `libs/*.py`.
6. **Where to look for examples.** Pointers to a small bundle, a complex
   bundle, and a node file.
7. **Where this doc lives.** Note that `CLAUDE.md` is a symlink to this file.

## 5. Per-area `AGENTS.md` content

**Rule.** An area `AGENTS.md` describes how that area works — mechanisms,
conventions, how to add or modify. It does **not** enumerate contents.
Specifics live with the thing itself (docstrings, top-of-file comments) or
in a per-subdir `AGENTS.md` only when that subdir has its own non-obvious
conventions.

**Corollary.** Every `libs/*.py` and `hooks/*.py` starts with a one-line
module docstring. Every `bin/*` script starts with a `# purpose:` header
comment. Discovery is by `ls` + reading those headers, not by an index page.

Each area `AGENTS.md` has the same five-section shape (target 30–80 lines):

1. What's in this directory (one paragraph).
2. Conventions (naming, file structure, what each kind of file does).
3. How to add / modify (concrete steps for the most common change).
4. Pitfalls (area-specific gotchas).
5. See also (links to relevant `docs/agents/*` and example files).

Per-area specifics:

- **`bundles/AGENTS.md`** — bundle anatomy (`items.py`, `metadata.py`, `files/`,
  `templates/`), where helpers go, when to extract to `libs/`. Links out to
  `docs/agents/bundlewrap/items.md` and `metadata.md` for language-level detail.
- **`nodes/AGENTS.md`** — `eval()` loading mechanism via `nodes.py`, demagify
  magic-string syntax, naming convention pattern (`<location>.<role>.py`).
  **Pitfall:** because node files are `eval()`'d, no top-level imports — only
  expression-level constructs.
- **`groups/AGENTS.md`** — same `eval()` mechanism via `groups.py`, subdir
  purpose convention (`applications/`, `locations/`, `machine/`, `os/`),
  how `all.py` interacts, group-membership rules, inheritance order.
- **`libs/AGENTS.md`** — what libs are (importable from bundles via
  `repo.libs.<x>`), conventions for adding a helper, contribution rule
  (one-line module docstring required).
- **`hooks/AGENTS.md`** — bw hook lifecycle, when each event fires, how to
  write a hook.
- **`data/AGENTS.md`** — what `data/` is for (data sources templated and
  consumed by bundles), conventions for adding a new data source.
- **`items/AGENTS.md`** — what custom item types are, how to write one,
  when to use a custom item type vs a `file` item.
- **`bin/AGENTS.md`** — what `bin/` is for (operator tooling, not invoked by
  bundlewrap).

## 6. `docs/agents/` content

### `conventions.md` (~80–120 lines)

- **Secrets / demagify.** `!password_for:`, `!decrypt:`, `!decrypt_file:`,
  `!32_random_bytes_as_base64_for:`. What each does, where they're allowed
  (node files, evaluated through `nodes.py`), why agents must never echo
  decrypted values.
- **Custom bundlewrap fork.** How it's installed
  (`pip install --editable git+file:///…/bundlewrap-fork@main`), implications
  (don't assume upstream-only behavior), pointer to the fork source.
- **Group inheritance order** & how metadata merges
  (`all.py` → location → os → machine → applications → node).
- **Naming conventions** for nodes (`<location>.<role>.py`) and groups
  (subdir purpose).
- **Files agents must not modify.** `.secrets.cfg*`, `.venv`, `.cache`,
  `.bw_debug_history`, `.envrc`.

### `commands.md` (~80–120 lines)

**Side-effect model** (paragraph up front):

- `bundles/<x>/metadata.py` `defaults` and `@metadata_reactor` can write into
  *any* namespace (e.g. nextcloud's metadata writes into `apt.packages` and
  `archive.paths`). Changing it can ripple into other bundles' inputs.
- `libs/<x>.py` is imported by both `items.py` and `metadata.py` across many
  bundles — biggest blast radius.
- `groups/*.py` changes membership (which bundles a node gets) and merged
  metadata.
- `bw hash` is the primary integrated check because it captures bundle
  membership + metadata + items + file content.

**Read-only command reference** (one line each):
`bw hash`, `bw metadata`, `bw items`, `bw items <node> <id> -p`, `bw nodes`,
`bw groups`, `bw verify`, `bw debug`, `bw test`, `bw plot`. Each tagged
read-only.

**After-change checks, keyed by what you changed:**

| You changed | First check | Drill-in |
|---|---|---|
| `bundles/<x>/items.py` | `bw hash <node>` for a node with bundle `<x>` | `bw items <node> <id> -p`; `bw verify <node>` |
| `bundles/<x>/metadata.py` | `bw hash` for *all nodes including bundle `<x>`* (reactors can ripple beyond `<x>`'s namespace) | `bw metadata <node>`; `bw metadata <node> -k <key>` |
| `bundles/<x>/files/*` (template) | `bw hash <node>` | `bw items <node> <path> -p` |
| `groups/*.py` | `bw hash` every node in/near the group | `bw groups -n <node>`; `bw metadata <node>` |
| `libs/<x>.py` | `bw hash` **all** nodes (cheap, no network) — biggest blast radius | `bw debug` to inspect helper outputs |
| `nodes/<x>.py` | `bw hash <node>` | `bw metadata <node>` |
| `hooks/*.py` | re-run the `bw` command whose lifecycle the hook hooks | — |
| Anything | `bw test` — cheapest repo-level sanity | — |

**Mutating commands (forbidden without explicit user request).** `bw apply`,
`bw run`, `bw lock` — what each does and why agents must not invoke them
autonomously.

**Hash diff workflow.** Capture `bw hash > before.txt`, make change,
`bw hash > after.txt`, diff. Canonical pre/post comparison.

**Targeting.** How to scope to one node / one group (`-t`, group selectors).

### `bundlewrap/README.md` (~80 lines)

Mental model paragraph: nodes ← groups → bundles → items; metadata flow
(groups → node → metadata processors → bundle items); hooks vs items vs libs.
Glossary, one paragraph each: node, group, bundle, item, items.py, metadata.py,
metadata reactor, hook, lib, `repo.libs`. Folder index. Fork callout
(explicit "we use a fork — here's what differs (or 'nothing day-to-day')";
link to fork source). Links out to <https://docs.bundlewrap.org> for depth.

### `bundlewrap/items.md` (~200–300 lines)

The item types this repo actually uses — file, pkg_apt, svc_systemd, action,
symlink, group, user, … — with common attributes and examples drawn from
this repo. The dependency keyword glossary: `needs`, `needed_by`, `triggers`,
`triggered`, `triggered_skip_for`, `tags`, `cascade_skip`, `unless` — each
with one sentence and a real example. Custom item types from `items/`
(currently `download`). "When in doubt, see upstream items reference" with
a link.

### `bundlewrap/metadata.md` (~200–300 lines)

`defaults` dict semantics (deep-merge into resolved metadata, can write into
any namespace). `@metadata_reactor.provides(...)` contract: signature, return
shape, fixpoint resolution, when to declare `provides` narrowly vs broadly.
Vault integration: `repo.vault.password_for`, `repo.vault.random_bytes_as_base64_for`,
`repo.vault.decrypt`, `repo.vault.decrypt_file` — and how they tie back to
demagify magic strings in node files. `repo.libs.hashable.hashable(...)` for
putting dicts in sets — a pattern used heavily in this repo, worth explicit
example. Common pitfalls: reactor declared narrower than it writes; reactor
that doesn't reach fixpoint; reactor that reads a key it didn't declare reading.

## 7. Seed work & rollout

### Phase 1 — scaffolding (one PR-sized chunk)

1. Root `AGENTS.md` (Section 4) + `CLAUDE.md` symlink → `AGENTS.md`.
2. `docs/agents/bundlewrap/README.md`, `items.md`, `metadata.md` (Section 6).
3. `docs/agents/conventions.md` and `commands.md` (Section 6).
4. Per-area `AGENTS.md` for `bundles/`, `nodes/`, `groups/`, `libs/`, `hooks/`,
   `data/`, `items/`, `bin/` (Section 5).
5. `bundles/AGENTS.template.md` so future bundle docs have something to copy.
6. Docstring/header pass: add a one-line module docstring to any `libs/*.py`
   and `hooks/*.py` lacking one; `# purpose:` header to any `bin/*` script
   lacking one.

Order within Phase 1: root → bundlewrap folder → conventions → commands →
area docs → docstring pass → template. Each piece can be reviewed in
isolation; the work bisects cleanly.

Honest scope: the bundlewrap folder is ~600 lines of focused writing total
(80 + 250 + 250). The rest is shorter — area docs and conventions land in
30–120 lines each.

### Phase 2 — seed bundles (10)

Bundles selected empirically (node+group references and recent commit
activity, validated 2026-05-10):

**Usage hubs (6):**

1. `monitored` (12 node refs) — meta-bundle, often misunderstood.
2. `postgresql` (9 refs, 3 cross-bundle).
3. `wireguard` (8 refs, has own lib + bin script).
4. `php` (8 refs).
5. `apt` (6 refs, has own lib).
6. `nginx` (4 refs, web foundational).

**Recently active or complex (4):**

7. `telegraf` (9 cross-bundle refs, 6 recent commits) — monitoring snippets
   ripple across bundles.
8. `backup` (7 refs, cross-node coordination).
9. `letsencrypt` (6 refs, cross-cutting).
10. `nextcloud` (5 recent commits, complex, actively edited).

For each: write one `AGENTS.md` from the template — purpose, usage, metadata
dict, produces, depends-on, gotchas. Migrate any existing
`bundles/<x>/README.md` content into it and remove the old `README.md`.

### Phase 3 — leave-as-you-go

- Convention from this point: any time an agent (or you) materially edits a
  bundle, top-up or create its `AGENTS.md`. Documented as a rule in
  `bundles/AGENTS.md`.
- No mass-fill of the remaining ~95 bundles up front — most are simple enough
  that `items.py`/`metadata.py` are self-explanatory.

## 8. Future work (not this spec)

- Contributing an `AGENTS.md` to bundlewrap upstream (or to your fork)
  describing items/metadata semantics for agents — would shrink the
  bundlewrap folder over time and shift authority back upstream.
- Tooling: a read-only `bw` wrapper or lint that nudges new bundles toward
  having an `AGENTS.md`. Worth considering only after Phase 1+2 reveal which
  conventions actually drift.
- More bundlewrap docs files (`groups-nodes.md`, `hooks.md`) if real gaps
  surface during Phase 2 or Phase 3 work.

## 9. Open questions / risks

- **Risk: docs drift.** As the repo evolves, `AGENTS.md` files lag behind
  code. Mitigations: per-bundle docs are short (low maintenance); Phase 3
  rule attaches doc updates to material code edits; the area docs are
  mechanism-focused, which changes less often than enumerations.
- **Risk: bundlewrap-folder duplicates upstream.** Acknowledged trade-off.
  Mitigation: the folder is scoped to *as we use it here*, with explicit
  upstream links; not trying to be a full bundlewrap manual.
- **Open: which seed bundles to swap.** Phase 2 list is empirically grounded
  but not rigid — `zfs` (8 refs), `bind` (4 refs, own lib), and
  `routeros-monitoring` (15 recent commits, specialized) are honourable
  mentions if a swap is wanted later.
