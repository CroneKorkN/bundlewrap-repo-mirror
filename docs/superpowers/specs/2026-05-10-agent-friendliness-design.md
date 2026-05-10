# Agent-friendly repo — design

Date: 2026-05-10

## 0. Revisions

Material revisions since this spec was first written, kept here so anyone
reading the spec sees the current shape rather than the original intent.

- **Fork pivot.** Originally the spec planned a `docs/agents/bundlewrap/`
  folder (`README.md` + `items.md` + `metadata.md`) explaining
  bundlewrap-the-language inside ckn-bw. That folder is gone; the
  maintainer maintains a personal bundlewrap fork at
  `github.com/CroneKorkN/bundlewrap` whose root `AGENTS.md` carries the
  canonical agent-oriented bundlewrap-language reference. ckn-bw's docs
  link out to the fork instead. The venv installs editable from the fork
  (`-e git+https://github.com/CroneKorkN/bundlewrap.git@main`).
- **`commands.md` slimmed** from ~80–120 lines to ~30–50 lines: the fork's
  `AGENTS.md` carries the canonical bw runbook (read-only allowlist,
  after-change table, hash-diff workflow, `bw debug` sketch); ckn-bw's
  `commands.md` shrinks to repo-specific deltas (apt-key verification,
  `*.py_` suspended-node behavior, vault-echo guidance).
- **Phase 2 seed-list rebalance.** `php` swapped out for
  `routeros-monitoring` based on user-story analysis: php is a low-churn
  usage hub (8 refs but ~zero recent commits); routeros-monitoring is
  high-churn (15 commits in 18 months), exactly where seeded docs pay off
  most. See plan for empirical justification.
- **bw-syntax corrections** found by per-task code-review during the fork's
  AGENTS.md implementation, synced in: `bw items <node> <id> -p` does not
  exist (use bare or `--preview`); `bw hash` accepts only literal node /
  group names (selectors like `bundle:<x>` work for `bw nodes` etc., but
  not for `bw hash`); `bw groups -n <node>` does not exist (use
  `bw nodes <node> -a groups`).
- **Workflow + user-story validation findings** (16 small content adds
  across area docs, the per-bundle template, `commands.md`, and
  `conventions.md`) are recorded in the implementation plan rather than
  back-fitted into this spec — they're additions to file content, not
  scope changes.
- **Per-bundle docs are `README.md`, not `AGENTS.md`** (revised
  2026-05-10, after Phase 1 scaffolding landed). The spec originally
  specified one balanced `AGENTS.md` per bundle (§3 template) plus a
  Phase 2 seed migration that folded existing READMEs into new
  AGENTS.md files (§7). After Phase 1 landed, the maintainer flagged
  that the rigid template wouldn't survive contact with the existing
  READMEs (which range from one-paragraph balanced docs to operational
  scratchpads — see `bundles/{flask,dm-crypt,apt,nextcloud}/README.md`).
  Resolution: one `README.md` per bundle, no fixed shape, no template;
  Phase 2 dropped; existing READMEs stay in place under leave-as-you-go.
  Current convention lives in `bundles/AGENTS.md` "Per-bundle README".
  **Sections §3 and §7 are no longer authoritative — read them as
  pre-pivot intent only.**

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
  bundlewrap-fork install pointer, files-not-to-touch).
- `docs/agents/commands.md`: ckn-bw-specific deltas to the fork's bw
  runbook (apt-key verification, suspended-node behavior, vault-echo
  guidance). Canonical bw command reference lives in the fork's `AGENTS.md`.
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
│       └── commands.md         # ckn-bw deltas; canonical bw runbook is in
│                               # the fork's AGENTS.md (linked from here)
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
when a repo-specific idiom is in play → fork's `AGENTS.md` (at
`https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md`) for any
bundlewrap-language question (item types, dep keywords, metadata reactor
semantics).

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
   - Repo runs editable from the maintainer's bundlewrap fork
     (`github.com/CroneKorkN/bundlewrap`, branch `main`); behavior tracks
     upstream main but the fork's `AGENTS.md` is the canonical
     bundlewrap-language reference. See `docs/agents/conventions.md` for
     install detail.
   - Prefer adding helpers to `libs/` over duplicating logic across bundles.
3. **Layout map.** Terse, link-rich. One line per top-level dir, each linking
   to that area's `AGENTS.md`.
4. **How nodes/groups/bundles fit together.** 5–10 lines: nodes pick up bundles
   via groups; metadata flows from groups → node → metadata processors;
   `nodes.py` and `groups.py` (root) are the loaders that walk the dirs and
   run `demagify`.
5. **Conventions you must know.** One-line summary + link for each:
   - Fork's `AGENTS.md`
     (`https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md`) —
     read first if new to bundlewrap. Carries the safety envelope, the
     after-change runbook, and cheat-sheets for item dep keywords +
     `metadata.py` pitfalls.
   - `docs/agents/conventions.md#secrets` — secrets / demagify magic strings.
   - `docs/agents/conventions.md#bundlewrap-version` — install pointer
     (editable from the fork's `main`).
   - `docs/agents/conventions.md#groups` — group inheritance order.
   - `docs/agents/commands.md` — ckn-bw-specific deltas to the bw runbook
     (apt keys, suspended nodes, vault-echo guidance).
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
  the fork's `AGENTS.md` (item types, dep keywords, metadata reactor
  semantics) for language-level detail.
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
- **Bundlewrap version / install.** Repo runs editable from the maintainer's
  personal fork: `pip install -e git+https://github.com/CroneKorkN/bundlewrap.git@main#egg=bundlewrap`.
  Captured in `requirements.txt`. The fork's `main` tracks upstream main; the
  fork's `AGENTS.md` is the canonical bundlewrap-language reference.
- **Group inheritance order** & how metadata merges
  (`all.py` → location → os → machine → applications → node).
- **Naming conventions** for nodes (`<location>.<role>.py`) and groups
  (subdir purpose).
- **Files agents must not modify.** `.secrets.cfg*`, `.venv`, `.cache`,
  `.bw_debug_history`, `.envrc`.

### `commands.md` (~30–50 lines)

The fork's `AGENTS.md` is the canonical bw runbook — read-only command
allowlist, after-change table, hash-diff workflow, `bw debug` sketch,
verified against 5.0.3 source. ckn-bw's `commands.md` carries only
repo-specific deltas:

- **One-line lead** pointing at
  `https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md` for the
  full runbook.
- **Apt-key after-change row.** Editing `data/apt/keys/*.{asc,gpg}` →
  first verify with `gpg --show-keys <newkey>` locally + fingerprint diff
  against the expected source. Trial via `bw apply` is the *failure* path
  (a wrong key blocks unattended upgrades cluster-wide). Not in the
  fork's runbook because it's repo-specific.
- **`*.py_` suspended-node interaction.** A node file ending in `.py_` is
  silently excluded from the loader; `bw nodes` won't list it. Document
  this so an agent doesn't think a node is missing when it's actually
  parked.
- **Vault magic-string handling.** Never echo decrypted output, even in
  `bw debug` exploration. Cross-link to `conventions.md#secrets`.

## 7. Seed work & rollout

### Phase 1 — scaffolding

Gated on: the fork's `AGENTS.md` exists and is reachable at the URL above
(verified 2026-05-10).

1. `docs/agents/conventions.md` (Section 6).
2. `docs/agents/commands.md` (Section 6).
3. Per-area `AGENTS.md` for `bundles/`, `nodes/`, `groups/`, `libs/`, `hooks/`,
   `data/`, `items/`, `bin/` (Section 5).
4. `bundles/AGENTS.template.md` so future bundle docs have something to copy.
5. Root `AGENTS.md` (Section 4) + `CLAUDE.md` symlink → `AGENTS.md` (written
   last so all internal link targets exist).
6. Docstring/header pass: add a one-line module docstring to any `libs/*.py`
   and `hooks/*.py` lacking one; `# purpose:` header to any `bin/*` script
   lacking one.

Order rationale: build link targets bottom-up (conventions → commands →
area docs → template), then root last, then the docstring pass last. Each
piece can be reviewed in isolation; the work bisects cleanly.

Honest scope: ~800–1000 lines of focused writing total now that
bundlewrap-language docs live in the fork. Area docs + conventions land
in 30–120 lines each; root `AGENTS.md` is ~150 lines.

### Phase 2 — seed bundles (10)

Bundles selected empirically (node+group references and recent commit
activity, validated 2026-05-10):

**Usage hubs (6):**

1. `monitored` (12 node refs) — meta-bundle, often misunderstood.
2. `postgresql` (9 refs, 3 cross-bundle).
3. `wireguard` (8 refs, has own lib + bin script).
4. `routeros-monitoring` (15 commits in 18 months — most-churned bundle).
5. `apt` (6 refs, has own lib).
6. `nginx` (4 refs, web foundational).

**Recently active or complex (4):**

7. `telegraf` (9 cross-bundle refs, 6 recent commits) — monitoring snippets
   ripple across bundles.
8. `backup` (7 refs, cross-node coordination).
9. `letsencrypt` (6 refs, cross-cutting).
10. `nextcloud` (5 recent commits, complex, actively edited).

(Original §0 noted: `php` was originally seeded but swapped for
`routeros-monitoring` after user-story analysis showed it's a low-churn
hub, while routeros-monitoring is the highest-churn target in the repo.)

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

- Tooling: a read-only `bw` wrapper or lint that nudges new bundles toward
  having an `AGENTS.md`. Worth considering only after Phase 1+2 reveal
  which conventions actually drift.
- Pushing the fork's `AGENTS.md` upstream to `bundlewrap/bundlewrap` —
  it's written in a style that allows it; a follow-up the maintainer
  may pursue.

## 9. Open questions / risks

- **Risk: docs drift.** As the repo evolves, `AGENTS.md` files lag behind
  code. Mitigations: per-bundle docs are short (low maintenance); Phase 3
  rule attaches doc updates to material code edits; the area docs are
  mechanism-focused, which changes less often than enumerations.
- **Risk: fork drifts from upstream.** ckn-bw's docs link to the fork's
  `AGENTS.md`; if the fork falls far behind upstream main, the linked
  semantics might not match what real bundlewrap users see. Mitigation:
  the fork tracks upstream main via periodic merges; ckn-bw's
  `requirements.txt` pins `@main` so the venv stays aligned with the
  fork's documented behavior.
- **Open: seed bundles.** Phase 2 list is empirically grounded but not
  rigid — `zfs` (8 refs), `bind` (4 refs, own lib), and `bootshorn`
  (recent burst target) are honourable mentions if a swap is wanted
  later.
