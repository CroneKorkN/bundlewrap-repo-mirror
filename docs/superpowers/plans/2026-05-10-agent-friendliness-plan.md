# Implementation plan — agent-friendliness docs

> **Note (post-execution):** This plan is a frozen pre-pivot artifact.
> It captures the approach as designed before Phase 1 landed and the
> per-bundle convention pivoted from `AGENTS.md` to `README.md`.
> Sections describing per-bundle `AGENTS.md`,
> `bundles/AGENTS.template.md`, and the Phase-2 seed-bundle migration
> reflect the original intent, not what shipped. For the current
> shape, read the spec's §0 Revisions
> ([`../specs/2026-05-10-agent-friendliness-design.md`](../specs/2026-05-10-agent-friendliness-design.md))
> and the handoff status note
> ([`../handoffs/2026-05-10-implementation-handoff.md`](../handoffs/2026-05-10-implementation-handoff.md)).
> Kept in tree as a record of how the work was scoped and what
> validation findings (workflow + user-story) shaped Phase 1.

## Context

This BundleWrap config repo (`ckn-bw`, ~22 nodes / 103 bundles) currently has
no agent-facing orientation: no `CLAUDE.md` / `AGENTS.md`, only ~10 of 103
bundles have a `README`, and the root `README.md` is a personal TODO. Agents
landing cold spelunk to figure out conventions (demagify magic strings,
`metadata_reactor` patterns, lib helpers, what's safe to run).

Goal: ship one PR that scaffolds the documentation surface described in
`docs/superpowers/specs/2026-05-10-agent-friendliness-design.md`, plus a
second PR seeding 10 high-value bundle docs. After this work, an agent can
land useful work in nodes / groups / bundles / libs without trial-and-error,
and never invokes a state-mutating `bw` command without explicit user request.

**Corrections since the spec was written.**

- Verification on 2026-05-10 found the active venv ran upstream `bundlewrap 4.24.0`,
  the README's fork install was stale, and the user has since upgraded the
  venv to PyPI `bundlewrap 5.0.3`.
- The user refreshed `/Users/mwiegand/Projekte/bundlewrap-fork` to track upstream
  master at commit `a97cdb13` (also version 5.0.3), and decided to make the
  fork agent-friendly *first* (separate session, separate plan), then return
  here. The ckn-bw plan therefore drops the `docs/agents/bundlewrap/` folder
  it originally planned — bundlewrap-language docs live in the fork now.

This plan reflects the reduced ckn-bw scope. It is gated on the fork's
`AGENTS.md` existing, since this repo's root `AGENTS.md` links out to it.
See the handoff document delivered separately for the fork-session work.

## Scope

Two PRs.

- **PR1 — scaffolding.** Root `AGENTS.md`, `CLAUDE.md` symlink, the
  `docs/agents/` tree (just `conventions.md` and `commands.md` — no
  `bundlewrap/` folder; that lives in the fork), all eight per-area
  `AGENTS.md` files, the per-bundle template, the docstring/header pass on
  `libs/*.py` / `hooks/*.py` / `bin/*`, and the README cleanup (remove the
  stale fork section, keep everything else). Spec correction in the same PR.
- **PR2 — seed bundles.** Per-bundle `AGENTS.md` for the 10 seed bundles;
  fold and remove any existing per-bundle `README.md` in those.

Phase 3 from the spec ("leave-as-you-go") is a convention, not a code task —
captured in `bundles/AGENTS.md` as a contribution rule.

## Approach (recommended)

### PR1 — scaffolding

Order is dependency-respecting; each step's output is referenced by later
steps' link targets.

**Precondition:** the fork's root `AGENTS.md` exists at
`/Users/mwiegand/Projekte/bundlewrap-fork/AGENTS.md`. PR1 links out to it,
so PR1 cannot land cleanly until the fork session has produced that file.

1. **Spec correction.** In
   `docs/superpowers/specs/2026-05-10-agent-friendliness-design.md`:
   - Replace "fork" framing with the actual reality: venv runs `bundlewrap
     5.0.3` (PyPI install today), the user maintains a separate fork at
     `github.com/CroneKorkN/bundlewrap` whose `master` tracks upstream and
     whose `AGENTS.md` is the canonical bundlewrap-language reference.
   - Replace the `docs/agents/bundlewrap/` folder content (Section 2 IA,
     Section 6) with a single bullet: "bundlewrap-language reference lives
     in the fork at `<URL>/AGENTS.md`; ckn-bw links to it from root
     `AGENTS.md` and `conventions.md`."
   - Update Section 4 quickstart and Section 6 `conventions.md` accordingly.
   - Single commit before any other ckn-bw docs are written.

2. **`docs/agents/conventions.md`** (~80–120 lines): demagify magic strings;
   bundlewrap version note (`5.0.3`, link to the fork's `AGENTS.md` for
   language reference); group inheritance order; node/group naming
   conventions; the `eval()` idiom in `nodes.py` / `groups.py` and what
   that constrains for editors/agents (no top-level imports, etc.);
   do-not-touch file list (`.secrets.cfg*`, `.venv`, `.cache`,
   `.bw_debug_history`, `.envrc`).

3. **`docs/agents/commands.md`** (~30–50 lines, slimmed). The fork's
   `AGENTS.md` (at `https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md`)
   now carries the canonical bw runbook — tiers, after-change table,
   hash-diff workflow, `bw debug` sketch — verified against 5.0.3 source.
   This file shrinks to ckn-bw-specific deltas:
   - One-line lead pointing at the fork's `AGENTS.md` for the canonical
     read-only allowlist + after-change runbook.
   - **Apt-key after-change row** (S7 finding): editing
     `data/apt/keys/*.{asc,gpg}` → first verify with
     `gpg --show-keys <newkey>` locally + fingerprint diff against the
     expected source. Trial via `bw apply` is the *failure* path (a wrong
     key blocks unattended upgrades cluster-wide). Not in the fork's
     runbook because it's repo-specific.
   - **`*.py_` suspended-node interaction with `bw nodes`**: a node file
     ending in `.py_` is silently excluded from the loader; `bw nodes`
     won't list it. Document this so an agent doesn't think a node is
     missing when it's actually parked.
   - **Vault magic-string handling**: never echo decrypted output, even
     in `bw debug` exploration. Cross-link to `conventions.md#secrets`.

4. **Per-area `AGENTS.md`** — eight files, mechanism-focused, no
   enumeration. Order: `bundles/`, `nodes/`, `groups/`, `libs/`, `hooks/`,
   `data/`, `items/`, `bin/`. Each ~30–80 lines, same five-section shape
   from spec Section 5.

5. **`bundles/AGENTS.template.md`** — the per-bundle template (spec
   Section 3 verbatim, with placeholder text in each section).

6. **Root `AGENTS.md`** — written so all link targets exist. Spec
   Section 4, with the "Conventions you must know" first bullet now
   pointing at the fork's `AGENTS.md` (canonical bundlewrap language)
   instead of an internal `bundlewrap/` folder. Quickstart bullet about
   the fork updated to: "bundlewrap reference lives in `<fork-URL>` —
   read first if new to bundlewrap." Then create `CLAUDE.md` as a symlink:
   `ln -s AGENTS.md CLAUDE.md`.

7. **Docstring/header pass** — for every `libs/*.py` and `hooks/*.py`
   without a top-of-file module docstring, add a one-liner. For every
   `bin/*` script without a header comment, add a `# purpose: …` line. Do
   not touch files that already have one. Mechanical: read each file's
   first ~10 lines, decide, edit only if missing.

8. **Root `README.md` cleanup** — remove the stale "install bw fork"
   section (the `pip3 install --editable git+file:///…/bundlewrap-fork…`
   block) since the venv runs PyPI 5.0.3. Leave the rest of the README
   untouched.

### PR2 — seed bundles

For each of the 10 seed bundles, write `bundles/<name>/AGENTS.md` from
`bundles/AGENTS.template.md`. Where a bundle already has `README.md`, fold
its content into the new `AGENTS.md` and remove the old `README.md` in the
same commit.

Seed list (from spec Section 7, validated empirically 2026-05-10):

| # | Bundle | Existing README? | Notes |
|---|---|---|---|
| 1 | `monitored` | check | meta-bundle, often misunderstood |
| 2 | `postgresql` | check | foundational |
| 3 | `wireguard` | check | own lib + bin script |
| 4 | `routeros-monitoring` | no | most-churned bundle (15 commits / 18mo); replaces `php` per user-story rebalance |
| 5 | `apt` | check | own lib |
| 6 | `nginx` | check | web foundational |
| 7 | `telegraf` | check | high cross-bundle ripple |
| 8 | `backup` | check | cross-node coordination |
| 9 | `letsencrypt` | check | cross-cutting |
| 10 | `nextcloud` | yes (verified) | complex, recent activity |

For each: derive `Metadata` dict by reading the bundle's `metadata.py` and
running `bw metadata <one-node-with-the-bundle>` to confirm the resolved
shape. Derive `Produces` from `items.py`. Derive `Depends on` by checking
which other bundles' artifacts (apt packages, systemd services) the
bundle's reactors and items reference. Use the ccc index (built 2026-05-10)
for fast cross-bundle lookups when filling `Depends on`.

## Workflow validation findings (2026-05-10) — content additions

Traced the "implement a new bundle" workflow against the planned docs.
Natural agent path is root → `bundles/AGENTS.md` → example bundle → write
files → wire to a node → verify. Seven gaps found; six are one-line
additions to `bundles/AGENTS.md`, one is a rewrite of root §6's example
pointers (~8 lines). All low-cost; fold into the corresponding files when
written in PR1.

1. **`bundles/AGENTS.md` — "Before you start" header.** `conventions.md`
   is off the natural path; call it out as required reading at the top,
   not just in "see also." This repo's idioms (vault calls in reactors,
   `repo.libs.hashable.hashable(...)`, demagify) live there. An agent
   who skips it will write subtly wrong code (e.g. dict-in-set
   `TypeError`, vault calls in the wrong place).

2. **Root `AGENTS.md` §6 — use-case keyed example pointers.** Replace the
   spec's "small bundle / complex bundle / node file" with one-line
   pointers per pattern: vault usage, templated files, cross-bundle
   reactor writing, `download` custom item. Pick concrete bundles at write
   time (grep for the patterns to find good exemplars). ~8 lines.

3. **`bundles/AGENTS.md` "How to add" — explicit wiring step.** Add a
   numbered step: "(4) Wire to nodes — see `groups/AGENTS.md` for
   application-style group wiring or `nodes/AGENTS.md` for direct
   attachment via a node's `bundles` list." Currently the wiring step is
   implicit; agent has to discover by cross-reading two area docs.

4. **`bundles/AGENTS.md` Conventions — bundle naming.** One line:
   bundle directory names are lowercase with hyphens (e.g. `backup-server`,
   `bind-acme`, `dm-crypt`); avoid underscores. Verify the convention by
   `ls bundles | grep _` before writing — if the convention is mixed,
   document the actual rule.

5. **`bundles/AGENTS.md` "See also" — items and templates.** Cross-link
   to `items/AGENTS.md` (for the `download` custom item and how to write
   new custom item types) and to the fork's
   `docs/content/guide/item_file_templates.md` (template syntax). Both
   are common needs an agent writing a new bundle hits early.

6. **`bundles/AGENTS.md` — first-thing-to-run after writing.** One-liner
   pointing at `commands.md` with the canonical sequence: `bw test`
   (sanity) → `bw items <node>` (do items show up?) → `bw hash <node>`
   (changed as expected?). Saves the agent from hunting the runbook.

7. **`bundles/AGENTS.template.md` — empty-section guidance.** Add a note
   at the top of the template: "For a brand-new bundle without consumers
   yet, leave `Depends on` and `Produces` empty or marked TBD; fill in
   after the first verify run."

## User-story validation findings (2026-05-10) — additional content adds

Empirical user-story extraction from 1169 commits (full history, with
detailed analysis of the last 222 commits / 18 months) is at
`docs/superpowers/specs/2026-05-10-user-stories-from-history.md`. It
identified 21 recurring user stories. Coverage assessment vs the planned
docs: 5 ✅ / 13 ⚠ / 3 ❌. Below are the 16 additional content adds, grouped
by target file. Each is one paragraph or less. The ❌ items shape an
agent's *judgment* (highest value); the ⚠ items shape lookups.

### Root `AGENTS.md`

- **F9 — Personal TODO callout.** "Note: `README.md` is the maintainer's
  personal scratchpad, not project documentation. Onboarding lives here in
  `AGENTS.md`." One sentence in §1 ("What this repo is").

### `docs/agents/conventions.md`

- **S4 ❌ — Iterative-commit workflow style.** "User commits are
  iterative checkpoints, not landing-ready snapshots. Terse messages
  (`+`, `fix`, `whitespace`, `dowsnt exist`) and successive 'fix' commits
  on the same file are normal. Don't rebase WIP without asking. As an
  agent, prefer to land complete-feeling commits rather than mimic the
  iterative style."
- **S5 ❌ — Burst-state awareness.** "Before writing into a subsystem,
  check `git log --since='1 month ago' bundles/<x>` (or `nodes/<x>.py`,
  etc.). If it shows ≥10 recent commits, the subsystem is in flux and
  your assumptions about its metadata shape may already be stale. Read
  the most recent diffs first."
- **S11 ❌ — Suspension idiom ("for now / disable / dummy / offline").**
  "Commits with these markers indicate deliberate suspension, not bugs.
  If you encounter a stub or commented-out block, check
  `git log -- <file>` for the suspension reason before re-enabling. The
  user reverses these manually when ready."
- **F6 — `_old` / `_old2` soft-delete pattern.** "Suffixed-with-`_old`
  directories are the user's recovery buffer during big refactors. Don't
  delete them without asking, even if they look orphaned."
- **F8 — Branch naming for PRs.** "PRs go through self-hosted
  Gitea/Forgejo. Branch names are lowercase-snake_case descriptive
  (`debian-13`, `htz.mails_debian_13_squash`, `l4d2_the_next`)."
- **S20 — Bundlewrap version-migration recipe (optional).** "When the
  next major bw version lands: read upstream migration guide → grep for
  affected reactor patterns → rewrite each → bump `requirements.txt`
  last." Captures the pattern from `186d503` (bw 4 → 5). Useful given
  the maintainer's tool-design pivot.

### `docs/agents/commands.md`

- **S7 — Apt-keys verification.** Add a row to the after-change table:
  `data/apt/keys/*.{asc,gpg}` → first check is `gpg --show-keys
  <newkey>` locally + visual diff against expected fingerprint. Trial
  via `bw apply` is the *failure* path (a wrong key blocks unattended
  upgrades cluster-wide).
- ~~**S21 — `bw debug` content sketch.**~~ Resolved upstream: the fork's
  `AGENTS.md` now carries the canonical `bw debug` content sketch (probes
  for `repo.get_node(...).metadata`, `repo.libs.<x>`, `repo.path`). No
  ckn-bw addition needed — Approach step 3 already points at the fork.

### `bundles/AGENTS.md`

- **S3 — Template recognition.** One paragraph: "Files under
  `bundles/<x>/files/` are static unless the `file:` item declares
  `content_type='mako'` or the file extension triggers templating
  (see fork's `docs/content/guide/item_file_templates.md`). To check:
  read the matching `file:` entry in `items.py`."
- **S13 — How to remove a bundle.** 5-line section, symmetric to "How
  to add": "(1) `git grep '<name>'` to find references in nodes/groups/
  other bundles; (2) remove those references; (3) `rm -rf bundles/<x>/`;
  (4) `bw test` and `bw nodes` to confirm clean."
- **S18 — README transition state.** "If a bundle has both `README.md`
  and `AGENTS.md`, `AGENTS.md` is canonical; the README is being phased
  out. ~23 bundle READMEs remain after the seed PR — Phase 3 leave-
  as-you-go folds them in over time."

### `bundles/AGENTS.template.md`

- **S12 — Optional `## Writes into` section.** Add to template (after
  `## Depends on`): "List other namespaces this bundle's `defaults` or
  reactors write into (e.g. nextcloud writes into `apt.packages` and
  `archive.paths`). Skip section if none — most bundles don't write
  cross-namespace, but the ones that do create the highest-blast-
  radius surprises."

### `nodes/AGENTS.md`

- **S2 — Silent eval-load-failure pitfall.** "Node files are `eval()`'d.
  A syntax error or top-level `import` causes the loader to silently
  drop the node. If `bw nodes` reports fewer nodes than expected, check
  `groups.py` (the user added explicit error printing in commit
  `dc40295` after being bitten)."
- **S9 — `*.py_` suspend convention.** "Appending `_` to a node
  filename (e.g. `htz.l4d2.py_`) parks it without loading. Used to keep
  decommissioned-but-not-deleted node configs in tree."
- **S9 — Symmetric "How to add a node" workflow.** Numbered steps
  parallel to `bundles/AGENTS.md` "How to add": (1) create
  `nodes/<location>.<role>.py` with `eval()`-safe expression syntax,
  (2) populate `id`, `hostname`, `groups`, `bundles`, `metadata`, (3)
  add to relevant `groups/<area>/<x>.py` if group membership is the
  attachment point, (4) verify with `bw nodes`, `bw nodes <node> -a groups`,
  `bw metadata <node>`.
- **S19 — Node-rename failure mode.** "Renaming a node file renames
  the node. Vault entries (via `!password_for:<node>`), `bw hash`
  records, and ssh known_hosts associations all key on node name —
  search and replace before renaming, or vault lookups silently
  return new (wrong) values."

### `groups/AGENTS.md`

- **S10 — Family-file pattern.** "OS variants commonly share a
  `*-common.py` parent (e.g. `debian-13-common.py` shared by
  `debian-13.py` and `debian-13-pve.py`). Use this when introducing
  related-but-distinct OS group families."
- **S10/S15 — New-OS-variant recipe.** "To introduce a new OS major:
  (1) add `groups/os/debian-N.py` + `debian-N-common.py` parallel to
  the existing files (don't edit in place); (2) add
  `data/apt/keys/debian-N-*.{asc,gpg}`; (3) bump dependent bundles
  that branch on OS string (e.g. `bundles/bind/items.py`); (4) bump
  affected nodes' `groups` lists one at a time; (5) delete the old
  OS file when no node references it."

### `data/AGENTS.md`

- **S7 — Two distinct content models.** "`data/apt/keys/` holds binary
  GPG keys consumed by `bundles/apt`; `data/grafana/rows/` holds Python
  modules for Mako-templated dashboards. Same directory shape, different
  content models — when adding a new data subdir, declare which model
  it follows."
- **F4 — `data/` vs `bundles/<x>/files/` heuristic.** "If a data asset
  is read by exactly one bundle, prefer `bundles/<x>/files/`. Use
  `data/` for shared/multi-consumer artifacts. Single-instance evidence:
  `78a8abc` moved `mikrotik.mib` from data/ into the bundle for this
  reason."

### `hooks/AGENTS.md`

- **S17 — Broken-hook failure mode.** "A hook that errors at load time
  breaks every `bw` command that fires that lifecycle (including
  `bw test`, defeating the obvious diagnostic). Test new hooks in
  isolation first: `bw debug` then `import sys; sys.path.insert(0,
  'hooks'); import <hookmodule>`. Iterate there until the import is
  clean."

### `libs/AGENTS.md`

- **S16 — Find-consumers snippet.** Add as a one-liner under
  Pitfalls: "Before changing a lib's API, find consumers:
  `git grep -l 'repo.libs.<x>'`. Lib changes have repo-wide blast
  radius — every bundle that imports the lib re-evaluates."

### `bin/AGENTS.md`

- **S14 — `bin/script_template`.** "When introducing a new operator
  script, start from `bin/script_template` (the user maintains it as
  the canonical starter)."

## Phase 2 seed list rebalance

User-story analysis (story 5, subsystem-burst evidence) found that 3 of
5 recent burst targets are unseeded. Strongest single swap:

- **Drop `php`** (8 node refs but ~zero recent commits — usage hub that
  doesn't change). Add **`routeros-monitoring`** (15 recent commits, the
  most-touched bundle in 18 months; not a dependency hub but high churn).

Optional second swap (judgment call):

- **Drop `apt`** (6 refs, has own lib, foundational but stable) and add
  **`bootshorn`** (recent burst target, has its own subsystem). Or keep
  `apt` for usage-hub coverage and accept that the seed misses bootshorn
  — Phase 3 covers it lazily.

Default this plan to the **single swap** (php → routeros-monitoring);
note `apt → bootshorn` as a second-swap option if the user wants it.

## Critical files

**New:**

- `AGENTS.md` (root)
- `CLAUDE.md` (symlink → `AGENTS.md`)
- `docs/agents/conventions.md`
- `docs/agents/commands.md`
- `bundles/AGENTS.md`, `bundles/AGENTS.template.md`
- `nodes/AGENTS.md`, `groups/AGENTS.md`, `libs/AGENTS.md`,
  `hooks/AGENTS.md`, `data/AGENTS.md`, `items/AGENTS.md`, `bin/AGENTS.md`
- `bundles/{monitored,postgresql,wireguard,routeros-monitoring,apt,nginx,telegraf,backup,letsencrypt,nextcloud}/AGENTS.md`

**Modified:**

- `docs/superpowers/specs/2026-05-10-agent-friendliness-design.md` (fork → upstream correction).
- `README.md` (remove stale "install bw fork" section).
- `libs/*.py`, `hooks/*.py` (add module docstrings where missing).
- `bin/*` (add `# purpose:` header where missing).

**Deleted:**

- `bundles/<name>/README.md` for each of the ~10 seed bundles that have one
  (content folded into `AGENTS.md`).

## Existing utilities & assets to reuse

- **Spec** at `docs/superpowers/specs/2026-05-10-agent-friendliness-design.md` —
  the source of truth for what each file contains. Sections 3, 4, 5, 6 of
  the spec are nearly copyable into the actual files.
- **User-story validation doc** at
  `docs/superpowers/specs/2026-05-10-user-stories-from-history.md` —
  21 stories grounded in git history with concrete commit evidence.
  When writing per-bundle docs, look up the relevant story for evidence
  of typical changes (e.g. for `nextcloud`, see Story 1 + Story 5
  l4d2-style burst comparison). The "Implications for agent docs"
  paragraphs in each story map directly to the additions in §"User-
  story validation findings" above.
- **ccc index** built at `.cocoindex_code/` on 2026-05-10 (768 chunks, 340
  files) — useful in PR2 for finding bundles that consume a metadata key
  or import a particular lib.
- **Bundlewrap CLI** for verification: `bw metadata <node>`, `bw items <node>`,
  `bw test`, `bw hash`. Read-only; safe to run during writing.
- **Existing bundle READMEs** at `bundles/{freescout,influxdb2,dm-crypt,gcloud,flask,nextcloud,build-server,raspberrymatic-cert,letsencrypt,nodejs}/README.md`
  (and any others — verify with `find bundles -name README.md`) — content
  to fold into the matching `AGENTS.md`. These are the only existing
  human-prose source for those bundles; do not lose information when migrating.

## Verification

Run after PR1:

1. `bw test` — repo-level sanity (passes today; should still pass).
2. `bw nodes`, `bw groups`, `bw bundles` — sanity that loaders work after
   the docstring/header additions.
3. Check every internal link in `AGENTS.md` and `docs/agents/**.md`
   resolves to a real file. A tiny shell loop with `grep -oE '\]\([^)]+\.md[^)]*\)'`
   then `test -f` each path.
4. `readlink CLAUDE.md` resolves to `AGENTS.md`.
5. `grep -L '"""' libs/*.py hooks/*.py` reports zero files (every lib/hook
   has a module docstring).
6. `grep -L '^# purpose' bin/*` reports zero non-binary scripts.
7. `git grep -i "bw fork\|bundlewrap-fork"` reports only the corrected
   docs locations (no leftover fork references in `README.md`).
8. **Workflow walk-through.** Trace the "implement a new bundle" path
   end-to-end against the written docs: root → `bundles/AGENTS.md` →
   example pointer → can the writer locate vault/hashable/template
   guidance from there without spelunking? Confirms the §"Workflow
   validation findings" fixes actually closed the gaps.

Run after PR2:

1. `bw test` — still green.
2. For each seed bundle `<x>`: pick one node that has it, run
   `bw metadata <node>` and confirm the keys listed in
   `bundles/<x>/AGENTS.md` `Metadata` section actually appear in the
   resolved metadata. Catches drift between docs and reality.
3. `find bundles -name README.md` — confirm none exist for the 10 seed
   bundles (folded into `AGENTS.md`).
4. Each new `bundles/<x>/AGENTS.md` follows the template structure
   (`grep -L '^## Metadata' bundles/*/AGENTS.md` reports zero).

## Non-goals (re-asserted from spec)

- No tooling changes (no `bw` wrapper, no Makefile, no lint, no CI).
- No code refactoring, renaming, or splitting bundles.
- No mass-fill of the remaining ~93 bundles up front.
- No upstream contribution to bundlewrap (acknowledged future work).
- The root `README.md` keeps everything except the fork section.

## Risks & mitigations

- **Drift between docs and code.** Mitigation: per-bundle docs are short
  (low maintenance), the area docs are mechanism-focused (changes less
  often than enumerations), and PR2 verification step 2 catches metadata
  drift at write time.
- **PR1 is gated on the fork's `AGENTS.md` existing.** If you want to
  start ckn-bw work before the fork session lands, you can stub the link
  to the fork's `AGENTS.md` (e.g. point at the repo URL even if the file
  isn't there yet) and merge PR1, but that risks broken links if the fork
  URL or filename changes. Cleaner: do the fork session first, then PR1.
- **PR1 is now a moderate writing chunk** (~800–1000 lines instead of
  ~1500–2000), since the bundlewrap folder moved out. Single PR is
  comfortable. The user-story validation findings (16 small adds) push
  it to ~1000–1200; still manageable as one PR.
- **README undercount.** The plan/spec estimated ~10 existing bundle
  READMEs to fold; actual is **33** (verified 2026-05-10 from git
  history). The seed list intersects with only 4–5 of those (nextcloud
  has one verified; others — `find bundles -name README.md` will
  enumerate). PR2 only folds READMEs in seed bundles; ~28 remain
  untouched, addressed lazily by Phase 3. `bundles/AGENTS.md` notes
  this transition state explicitly (per user-story finding §S18) so
  agents reading both don't get confused.
