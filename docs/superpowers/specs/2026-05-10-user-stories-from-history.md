# User stories — derived from ckn-bw git history

Date: 2026-05-10
History range examined: first commit `572e29e` (2021-06-11) … HEAD `c03b033` (2026-05-10), total 1169 commits. Detailed per-file analysis covers the last 18 months (222 commits, 2024-11 → 2026-05); subject-line scans extended back 36 months for context. The pre-2024 history is dominated by the same patterns at lower velocity, so deeper sampling there did not surface new stories.

## Methodology

Three passes:

1. **Bulk extraction.** `git log --since="18 months ago" --name-status -M -C` written to `/tmp/ckn-bw-history.txt`. 1023 lines covering all 222 recent commits with file changes and rename/copy detection. This is the primary corpus.
2. **Frequency analysis.** Per-bundle / per-node / per-area churn counts; first-word commit-message frequency; A/M/D/R action breakdown (461 modifies, 95 adds, 22 deletes, 9 renames over the window); rename pairs extracted for naming-convention inference.
3. **Targeted spot reads.** `git show --stat` and full diffs on 10 commits representative of the high-stakes / cross-cutting / burst patterns (bw5 migration `186d503`, telegraf reactor refactor `4959461`, wol-waker scope-down `985a15e`, l4d burst seed `3469d98`, mailman introduction `d3b8e2e`, debian-13 `c41e6f8`, etc.) to verify intent matches message.

Clustering rule: a story is a recurring **user intent**, not a recurring **file pattern**. Two commits both touching `metadata.py` may be different stories. Aimed for stories with ≥3 grounding commits each. Final count: 19 stories.

The prior pass produced 12 stories. This pass adds 7 (investigation, trial-and-error microbursts, disable-for-now, cleanup-of-dead-code, subsystem deep-dive bursts, README touch-ups, naming-convention renames) and subdivides several of the original twelve.

## Story index

Ordered by frequency, recent-window unless noted.

1. **S1 — Tune one bundle's metadata** (~50+ commits). Small targeted `metadata.py` edits.
2. **S2 — Tweak one node's config** (~80+ commits, top-heavy). Per-node tuning, often serial.
3. **S3 — Edit a file template** (~40+ commits). `bundles/<x>/files/*` changes.
4. **S4 — Trial-and-error microburst** (frequent within bursts; ~15 burst-clusters). Successive "fix"/"+"/"wip" commits.
5. **S5 — Subsystem deep-dive burst** (5 major bursts in 18 months: l4d2, routeros, routeros-monitoring, bootshorn, debian-13).
6. **S6 — Modify items.py for a bundle** (~30 commits). Item logic / dep tweaks.
7. **S7 — Templated data update** (~15 commits). `data/apt/keys/*`, `data/grafana/rows/*`.
8. **S8 — Add a new bundle** (10 in 18 months: yourls, mailman, routeros, routeros-monitoring, pppoe, bootshorn, kea-dhcpd, proxmox-ve, ifupdown, network).
9. **S9 — Onboard a new node** (10 nodes added in 18 months).
10. **S10 — Group adjustment / new OS variant** (~12 commits). `groups/os/*`, `groups/locations/*`.
11. **S11 — Disable temporarily / "for now"** (~10 commits). Commenting out, dummy-ifying.
12. **S12 — Cross-bundle metadata-reactor refactor** (4 high-impact commits in 18 months).
13. **S13 — Cleanup / delete obsolete code** (~8 commits). `_old` bundles, removed nodes.
14. **S14 — Add or revise an operator script** (`bin/`) (~8 commits, 4 new scripts in 18 months).
15. **S15 — OS-version upgrade campaign** (3 campaigns: debian-12, debian-13, trixie/server-only).
16. **S16 — Add/modify a lib** (`libs/`) (5 commits in 18 months; 1 new lib).
17. **S17 — Add/modify a hook** (`hooks/`) (4 commits in 18 months; 2 new hooks).
18. **S18 — Per-bundle README touch-up** (~8 commits, sporadic).
19. **S19 — Naming-convention rename** (4 renames in 18 months).
20. **S20 — Bundlewrap version migration** (1 commit, but uniquely high-stakes — counted because it shapes the maintainer's roadmap).
21. **S21 — Interactive `bw debug` investigation** (.bw_debug_history evidence).

(Numbering shows 21 because three are kept short — S20 is a single high-stakes commit, S17 / S21 are low-frequency but materially distinct workflows. Anything that did not reach ≥3 grounding events was rolled into cross-cutting findings.)

## Stories

### Story 1: Tune one bundle's metadata

**Pattern.** Open `bundles/<x>/metadata.py`, change a value or add a key, commit. The most common single-file edit. Often very small (`fix typo`, `relax telegraf collection`, `mailserver zfs params`). The change is *intra-bundle* — no reactor surprise; just adjusting a default the bundle itself reads.

**Frequency.** ~50 commits over 18 months across many bundles. Recent: `7f20c94` (telegraf deprecations, 2026-03-09), `a7c7aaf` (nc preview options, 2026-03-09), `5fab21b` (apt install ca-certificates, 2026-02-10), `0d35bc2` (linux relax icmp ratelimit, 2026-02-10), `5fb1ee5` (less annoying root passwords / users, 2025-08-09).

**Files typically touched.** Single file: `bundles/<x>/metadata.py`. Sometimes one paired sibling file when the new metadata has an items consequence (see Story 6 for pure items work).

**Variations.**
- (a) **Tune an existing value.** Change a number, add a member to a set, swap a string. ~70% of cases.
- (b) **Add a new key.** `'unattended-upgrades': {}` added to the apt packages dict in `186d503`; `apt install ca-certificates` in `5fab21b`.
- (c) **Restructure a sub-tree for new behavior.** Less common; tends to bleed into Story 12 if it changes a reactor's contract.

**Evidence.**
- `7f20c94` (2026-03-09) — telegraf deprecations (2 files: bundles/routeros-monitoring/metadata.py + bundles/telegraf/items.py).
- `0d35bc2` (2026-02-10) — `linux relax icmp ratelimit` (1 file).
- `5fab21b` (2026-02-10) — `apt install ca-certificates` (1 file).
- `a0f5f80` (2026-01-11) — typo fix in routeros-monitoring metadata.
- `bdb9fa0` (2025-06-22) — `gitea disable registration` (changes `bundles/gitea/files/app.ini` template — boundary case with Story 3).

**Co-modification.** Usually none — single file. Occasionally pulls in `items.py` if the new key changes which file/service item is rendered. Almost never touches nodes (the value sits in defaults, nodes don't need to opt in unless a top-level key didn't exist before).

**Stakes.** Routine when the bundle's metadata is read only by itself. Moderate when the bundle uses cross-bundle reactor writes (e.g. telegraf, monitored). The maintainer's mental model assumes "metadata.py change → only the bundles using this bundle are affected"; that's only true if the bundle keeps to its own namespace. See Story 12 for the cross-bundle case.

**Implications for agent docs.** Well-served by `bundles/AGENTS.md` plus per-bundle `AGENTS.md` (PR2). Agents need to know:
- The bundle's own resolved metadata shape — covered by per-bundle template's `Metadata` section.
- Whether *this* bundle writes into other namespaces (cross-bundle ripple) — must be in the per-bundle `Gotchas` for any bundle that does (telegraf, monitored, wol-waker, archive). `commands.md`'s after-change row already covers it generally, but a per-bundle callout shortens the agent's loop.
- After-change verification: `bw hash <node>` — the table in `commands.md` covers this. **No gap.**

### Story 2: Tweak one node's config

**Pattern.** Edit a single `nodes/<name>.py` to change something node-specific: an interface, a hostname, a group membership, a metadata override. The most common workflow, but heavily skewed to a few "hot" nodes — `home.router.py` (25 touches/18mo), `ovh.secondary.py` (29), `home.server.py` (16). Most edits are tiny.

**Frequency.** ~80 node touches in 18 months across 21 nodes. 70% concentrated in 5 nodes.

**Files typically touched.** Single node file. Occasionally two when the change is "move responsibility from node A to node B" (e.g. `5a8dc7e` 2025-12-03 moves wakeonlan to its own vlan, edits home.backups.py + home.router.py + home.switch-rack-poe.py + groups/os/routeros.py).

**Variations.**
- (a) **Per-application config tweak** (e.g. ovh.secondary l4d server config — see Story 5).
- (b) **Hardware/network shape change** (home.server "more swap"; "fan/motherboard sensors"; home.router "fix dhcp"; "fix ip").
- (c) **Group membership change** — adding/removing strings in the node's `groups` list. Cross-cuts with Story 10.
- (d) **Bundle attachment** — adding a bundle to the node's `bundles` list (rare; usually goes via group instead).

**Evidence.**
- `838da64` (2026-03-09) — home server fan/motherboard sensors (1 file).
- `fcd92db` (2026-03-09) — more swap (1 file, home.server).
- `4652a42` (2026-01-10) — disable zfs mirror for now (home.backups.py — also a Story 11 example).
- `60f29aa` (2025-08-24) — fix hue dhcp (home.hue).
- `0e78afe` (2024-11-23) — fix ip (home.router).

**Co-modification.** Often none. When the change is a group-membership shift, the receiving group's file (`groups/os/routeros.py`, `groups/locations/home.py`) gets a paired edit. Network-shape edits frequently pull in 2-3 nodes plus `bundles/network/metadata.py`.

**Stakes.** Routine for value tweaks; moderate when the node provides services others depend on (home.router, htz.mails). High if node-file syntax is broken — recall that `nodes/<x>.py` is `eval()`'d, so a syntax error or top-level `import` breaks the loader for all nodes (commit `dc40295` in 2025-06-22 added an explicit `print message on parsing group error` to `groups.py`, suggesting the user has been bitten by silent loader failures).

**Implications for agent docs.** `nodes/AGENTS.md` should call out:
- The `eval()` constraint (no top-level imports, only expression-level constructs) — already in spec §5.
- Where to find resolved metadata after the edit (`bw metadata <node>`) — covered by `commands.md` row "nodes/<x>.py".
- Naming convention `<location>.<role>.py` and how it's tied to the loader — covered.
- **Gap:** the `eval()` failure mode is silent; the user himself patched the loader to print a message. Worth an explicit *pitfall* in `nodes/AGENTS.md`: "if `bw nodes` reports nothing or fewer nodes than expected, you have an `eval()` error in a node file." Otherwise an agent will assume the file was loaded.

### Story 3: Edit a file template

**Pattern.** Open `bundles/<x>/files/<template>` (a Mako/plain-text/script file rendered by `file` items), change content, commit. Often more frequent than `metadata.py` for service-config-heavy bundles.

**Frequency.** ~40+ commits over 18 months. Top hits: `bundles/left4dead2/files/setup` (11 touches), `bundles/left4dead2/files/start` (6), `bundles/left4dead2/files/server.cfg` (4), `bundles/left4dead2/files/scripts/overlays/tickrate` (4), `bundles/bootshorn/files/temperature` (4).

**Files typically touched.** Single template file most of the time. Sometimes paired with `items.py` if the template's render context (`content_from`, conditionals) needs an `items.py` edit too.

**Variations.**
- (a) **Trivial edit** (one-line tweak in `nginx.conf`, a setting in `roundcube/files/config.inc.php`).
- (b) **Mako template logic change** (e.g. `data/grafana/flux.mako` — Mako-based dashboards).
- (c) **Whole-file rewrite** (less common — usually a new feature).

**Evidence.**
- `a629024` (2026-01-11) — `bundles/roundcube/files/config.inc.php`: smtp use domain name from cert.
- `bf38520` (2026-03-07) — comment out slow download workshop maps in l4d overlay file.
- `64f8691` (2025-08-09) — bind named.conf.local: zones.rfc1918 only affect recursive views.
- `e117aca` (2025-01-09) — `bundles/backup/files/backup_all`: don't stop on first error.

**Co-modification.** Often none. Pairs with items.py when the file's render context changes.

**Stakes.** Routine. Side effects don't ripple — the file is rendered once on the destination node. Templates with embedded scripts (e.g. `bundles/backup/files/backup_all` is a shell script) are a hidden risk: a bug there runs on production.

**Implications for agent docs.** `bundles/AGENTS.md` should mention `files/` at all (currently the spec template lists "files/, templates/" in the bundle anatomy section but doesn't say *which* files are rendered as templates vs static, or how to recognize Mako vs plain). Need:
- One paragraph: how the `file` item picks template vs static (default extension behavior, `content_from`, `content_type`).
- A pointer to the **fork's** `docs/content/guide/item_file_templates.md` — already noted in the plan's "Workflow validation findings" §5. **Confirmed needed.**
- For service-config-heavy bundles (left4dead2, bind, postgresql), per-bundle `Gotchas` should call out non-trivial template logic. Currently only nextcloud, mailman, freescout have ad-hoc READMEs — most are bare.

### Story 4: Trial-and-error microburst

**Pattern.** A series of 3-15 short commits in quick succession (often the same hour) that walk a single change toward working. Subjects like `fix`, `+`, `whitespace`, `dowsnt exist`, `fix indent`, `fix set not dict`. Usually one bundle or one node, sometimes a single file modified 5-10 times in a day. This is a *workflow style*, not a single change.

**Frequency.** ~15 burst-clusters in 18 months. Recurring, not anomalous. Examples: nftables fixes (2025-07-11: `e7c5fe9`, `5a1ce55`, `8829902`), bootshorn temperature tweaks (2025-07-13: `c1917d5`, `6f86abd`, `951fa63`), l4d2 setup script (10+ commits within hours on 2025-10-29), routeros-monitoring (consecutive small edits across 2025-12-13 / 12-16 / 12-30).

**Files typically touched.** One file, repeatedly. Sometimes two paired files (items.py + metadata.py).

**Variations.**
- (a) **Compile-fix burst.** "fix indent" / "fix set not dict" — Python typo / structural mistake immediately corrected.
- (b) **Behavior-tuning burst.** Successive value changes ("more swap", "more workshop maps", "tickrate", "nc preview").
- (c) **Apply-then-correct.** A change that broke something on the next `bw apply`, fixed in the next commit.

**Evidence.**
- `e7c5fe9` → `5a1ce55` → `8829902` (2025-07-11, all within the same day, all `bundles/nftables/`).
- `c1917d5` → `75017a9` → `6f86abd` → `951fa63` (2025-07-13, all `bundles/bootshorn/`).
- `19c1945` → `a9e4013` → `8391afd` → `d91b205` → `3311bfb` → `351ce24` → `9572ac8` (2025-10-29, all l4d2).

**Co-modification.** None — repeats on the same files.

**Stakes.** Low individually, but reveals important workflow context: **commits are not landing-ready snapshots — they are the user's iterative checkpoints.** This shapes everything: an agent that reads recent history to learn "how does the user write code" will see noise unless it understands this.

**Implications for agent docs.** Not a per-feature docs gap — but **highly relevant context for every agent**. Belongs in root `AGENTS.md` quickstart or `conventions.md`:
- "Commit messages are terse and frequently iterative; expect successive commits on the same file. Don't rebase the user's WIP commits without asking." (Style guidance for an agent commit-creating workflow.)
- Verification chain: agents should run `bw test` / `bw hash` *before* committing rather than relying on later "fix" commits — an agent's commits are more durable than the user's, since they tend to land in batches.
- **Currently neither covered.** ⚠ Partial gap — adjacent to spec §4 quickstart but not explicit.

### Story 5: Subsystem deep-dive burst

**Pattern.** Periods of 1-6 weeks where 80%+ of commits target one bundle/subsystem. This is Story 4 scaled up — instead of one day of microcommits, it's a multi-week project. The user is *learning the subsystem in production*: introducing it, finding issues, refining, often with cross-cutting touches (groups, nodes, libs) that wouldn't appear in a single-bundle story.

**Frequency.** 5 major bursts in 18 months, plus 2-3 minor ones.

| Burst | Window | Commits | Subsystem |
|---|---|---|---|
| **left4dead2 server rebuild** | 2025-08 → 2026-02 | ~50 | `bundles/left4dead2/`, `nodes/ovh.secondary.py` |
| **routeros / mikrotik switches** | 2025-06-29 → 2026-01-11 | ~30 | `bundles/routeros/`, `bundles/routeros-monitoring/`, `groups/os/routeros.py`, 4 switch nodes |
| **debian-13 upgrade** | 2025-08-09 → 2026-03-07 | ~15 | `bundles/dovecot/`, `bundles/redis/`, `bundles/bind/`, `groups/os/debian-13*`, multiple nodes |
| **bootshorn (laptop temperature monitoring)** | 2025-07-11 → 2025-08-24 | ~15 | new bundle from scratch + `home.bootshorn-laptop` node |
| **pppoe (telekom uplink)** | 2025-07-11 → 2025-08-03 | ~12 | `bundles/pppoe/`, `bundles/network/`, `bundles/nftables/`, home.router |

**Files typically touched.** Mixed: cluster around one bundle, with pulls into `groups/os/<x>.py`, the relevant node, sometimes a new lib (e.g. `libs/version.py` introduced in the routeros burst at `86d9b8b`).

**Variations.**
- (a) **Bring-up of a new capability** (routeros switches, pppoe, mailman, bootshorn) — touches multiple areas as scaffolding lands.
- (b) **Refactor of an existing capability** (l4d2 rebuild from August onward — note the `_old` bundles created and later deleted; the `3469d98` "next l4d2 server iteration" commit is the burst seed).
- (c) **Migration burst** (debian-13) — see Story 15.

**Evidence (one per burst seed and one mid-burst):**
- l4d2: seed `3469d98` (2025-08-24, "the next l4d2 server iteration"), mid-burst `9572ac8` (2025-10-29, "l4d2 dynamic overlays"), wind-down `ac8e7e2` (2026-02-10, "delete old l4d bundles").
- routeros: seed `85daf26` (2025-06-29, initial bundle + switches), mid `0e6a705` (2025-07-01, "routeros switches ok"), monitoring expansion `8539f59` (2025-12-13, "mikrotik snmp monitoring").
- bootshorn: seed `5274639` (2025-07-11, "bootshorn recording" — full bundle skeleton in one commit), tuning `75017a9` → `951fa63` (Story 4 microburst).

**Co-modification.** Heavy. Burst commits routinely touch a bundle + a group + 1-2 nodes + (sometimes) a lib + (sometimes) a hook.

**Stakes.** Cumulatively high. Each burst introduces or substantially reshapes a subsystem. Mid-burst, the subsystem is in flux — items.py and metadata.py contracts shift, file templates churn, the docs (if any) are stale. **An agent landing in a hot burst should be the most cautious, not the least.**

**Implications for agent docs.**
- The planned per-area docs and per-bundle docs cover the **steady state** but not the **burst state**. A burst-aware agent would need:
  - A way to know "this subsystem is in active flux" — derivable from `git log --since="1 month ago" --pretty=format:'' --name-only | grep <area> | wc -l`. Could be a one-liner in `bundles/AGENTS.md`'s "Pitfalls": "before writing into a subsystem, check `git log --since='1 month ago' bundles/<x>` — if it's hot, your assumptions about the metadata shape may already be stale."
  - The seed bundle list (Phase 2 in spec §7) **misses three of the five recent burst targets**: routeros (15 commits), routeros-monitoring (15), bootshorn (15), pppoe (12). Of those, only `wireguard` (8 refs) is on the seed list. The spec acknowledges routeros-monitoring as "honourable mention." **⚠ Recommend rebalancing seed list toward currently-hot subsystems**, since those are where doc absence costs the most agent time.
- **Gap.** The subsystem-burst pattern itself isn't documented anywhere planned. Could be one paragraph in `conventions.md` about "how this repo evolves" — it would let an agent recognize and respond to flux.

### Story 6: Modify items.py for a bundle

**Pattern.** Open `bundles/<x>/items.py`, add/remove/rewire a `file:`, `pkg_apt:`, `svc_systemd:`, `action:`, etc. Often paired with metadata.py if the new item reads from a key that didn't exist. The change is *what gets installed/managed*, not *with what value*.

**Frequency.** ~30 commits over 18 months that primarily target items.py.

**Files typically touched.** Single `items.py`. Frequently paired (a) `bundles/<x>/files/<new>` if a new file item is added, (b) `bundles/<x>/metadata.py` when the items.py reads a new metadata key.

**Variations.**
- (a) **Wire deps right** — `needs`/`needed_by`/`triggers` adjustments. Lots of these (`9733a55` 2025-06-22 "svc_systemd:systemd-networkd add .service to name"; `c244645` "kea deps"; `663116c` "/var/lib/mysql needs mysql user to exist"; `befdf5a` "fixmo mariadb dependency"; `fb22a01` "systemd fix dependency overwrite").
- (b) **Add a new managed file/service** — usually appears alongside an `items.py` skeleton in a bundle creation (Story 8).
- (c) **Fix permissions** (`6616ae7`, `43e7c1f` redis permissions; `e17b023` grafana permission).

**Evidence.**
- `9733a55` (2025-06-22) — `svc_systemd:systemd-networkd add .service to name`.
- `47b69f0` (2025-11-04) — `l4d items stop script` (adds a file item).
- `c244645` (2024-11-23) — `kea deps`.
- `b838935` (2025-08-09) — `dont purge sudoers`.
- `8066efb` (2025-12-03) — `routeros: also add comment to interface` (logical edit in items.py).

**Co-modification.** Frequently with the bundle's own `metadata.py`, occasionally with a node when an items.py change broke one specific node's resolved state.

**Stakes.** Routine for value/tag/dep tweaks. Moderate when restructuring an item's identity (renaming a file path, changing `name=` of an `svc_systemd:`) — a rename without redirect is **two state changes** (delete old, create new) which can cause a service flap.

**Implications for agent docs.** Covered by `bundles/AGENTS.md` (anatomy) and the fork's `AGENTS.md`/items reference (item-type semantics). The repo-specific gap:
- The custom `download:` item type from `items/download.py` is mentioned in the plan but its semantics aren't documented in any planned area doc beyond `items/AGENTS.md`. The bw5 migration commit `186d503` touched `items/download.py` — agents adding a `download:` item need to know the actual interface (`expected_state`/`actual_state`/`get_auto_attrs`) post-bw5. **⚠ Need explicit per-item-type docstring on `items/download.py`** (the docstring/header pass in PR1 step 7 should cover this; verify it does).
- Dependency-keyword vocabulary (`needs`, `triggers`, `triggered`, `cascade_skip`, etc.) lives in the fork's `AGENTS.md` per the plan. **No additional ckn-bw doc gap.** ✅

### Story 7: Templated data update (apt keys, dashboards)

**Pattern.** Two distinct sub-flavors that use the same `data/` directory mechanically:
- (a) **Apt key refresh** — replace a `.gpg` / `.asc` file with a freshly downloaded key. ~5 commits in 18 months. Mechanical but high stakes (a wrong key breaks `apt update` on every node using that source).
- (b) **Grafana dashboard edits** — `data/grafana/rows/*.py` and `data/grafana/flux.mako`. ~10 commits. Active design work, often tied to a bursting subsystem (e.g. routeros monitoring).

**Frequency.** 15+ data/ touches in 18 months.

**Files typically touched.**
- (a) Apt: `data/apt/keys/<src>.{gpg,asc}` — single file, sometimes 2-3.
- (b) Grafana: `data/grafana/rows/<row>.py` + sometimes `data/grafana/flux.mako`.

**Variations.**
- (a) Apt key replace (one-shot).
- (b) Apt key migration (e.g. `f0d1cf9` "new icinga apt key" added a `.gpg` and renamed the old `.asc` → `.asc_`, evidence the user keeps stale-but-not-removed keys around).
- (c) Grafana dashboard tweak (cosmetic).
- (d) Grafana new row (new monitoring source).

**Evidence.**
- `1907c38` (2026-01-07) — `data/apt/keys/influxdata.asc: update`.
- `487fdff` (2025-12-01) — update some apt keys (crystal, grafana).
- `f0d1cf9` (2024-11-23) — new icinga apt key.
- `da29405` (2026-01-11) — `data/grafana/rows/routeros_*: update names`.
- `4a4167e` (2025-12-13) — routeros grafana discards and errors (new rows).

**Co-modification.** Apt: usually only `data/apt/keys/`. Sometimes paired with `bundles/apt/metadata.py` if the source URL/format also changed. Grafana: usually paired with `bundles/grafana/items.py` or `bundles/grafana/metadata.py`.

**Stakes.** Apt: **high** (broken key → blocked unattended upgrades cluster-wide). Grafana: low (dashboard reads only).

**Implications for agent docs.** `data/AGENTS.md` (planned) needs to:
- Distinguish the apt-keys-as-data-source pattern from the grafana-rows-as-Python-dashboards pattern — they look the same at the directory level but have totally different content models.
- Call out the verification step for apt keys: trial via `bw apply` is *not* safe (it's the failure path). Better: gpg-verify the key locally before committing. **⚠ Likely gap** — `commands.md`'s after-change table doesn't have a row for `data/apt/keys/*` (it falls into "Anything"). One-line addition warranted.
- Grafana rows: covered by general-template guidance.

### Story 8: Add a new bundle

**Pattern.** Create `bundles/<name>/` from scratch — at minimum `items.py` + `metadata.py`, often `files/<file>`. Can be a single commit landing the skeleton or the seed of a deep-dive burst (Story 5).

**Frequency.** 10 new bundles in 18 months: yourls (2025-06-22), mailman (2025-06-29), routeros (2025-06-29), routeros-monitoring (2025-12-13), pppoe (2025-07-11), bootshorn (2025-07-11), kea-dhcpd (2024-09-18 inside `TOTAL FACKUP`), proxmox-ve (2025-06-22), ifupdown (2025-06-22), network/items.py (2025-07-10).

**Files typically touched.**
- Always: `bundles/<name>/items.py`, `bundles/<name>/metadata.py`.
- Often: 1-3 `bundles/<name>/files/<file>`.
- Often: a node file (`nodes/<x>.py`) — to attach the bundle.
- Sometimes: a group file (`groups/applications/<x>.py` or `groups/os/<x>.py`) when wiring as application/OS-level.
- Occasionally: `data/<name>/` for bundle-templated data.
- Sometimes: a README.md (mailman, pppoe, l4d2 — not consistent).

**Variations.**
- (a) **One-commit skeleton** (most common). E.g. `5274639` bootshorn brought the whole bundle in 5 files at once.
- (b) **Seed + burst.** Skeleton lands, then several follow-up commits refine (Story 4 + Story 5).
- (c) **Inside a megacommit.** `67d5a4b` "TOTAL FACKUP" added kea-dhcpd, linux items.py + metadata.py among 20+ other changes. Anti-pattern, but it happens.

**Evidence.**
- `5274639` (2025-07-11) — bootshorn introduction.
- `aeb0a4f` (2025-06-22) — `nodes/mseibert.yourls.py: introduce` (5 files: yourls bundle + node + data/yourls/).
- `d3b8e2e` (2025-06-29) — mailman (10 files added).
- `e4e3c57` (2025-07-11) — pppoe telekom (full bundle).
- `8539f59` (2025-12-13) — mikrotik snmp monitoring (routeros-monitoring bundle).

**Co-modification.** Always cross-area: bundle + node, often + group. This is the canonical "wire it in" workflow.

**Stakes.** Moderate to high. A new bundle wired wrong (group memberships off, missing dep, reactor that overlaps a sibling's namespace) can break unrelated nodes' apply.

**Implications for agent docs.**
- Spec §3 per-bundle template is good shape — covers Metadata, Produces, Depends on, Gotchas.
- Plan workflow validation finding §3 already calls out the explicit-wiring step. ✅
- **Open question.** The seed bundle list for Phase 2 (`monitored, postgresql, wireguard, php, apt, nginx, telegraf, backup, letsencrypt, nextcloud`) was chosen for usage hubs + recent activity. Of the 10 *recently introduced* bundles in this story, only mailman and bootshorn would be obvious targets, and neither is on the seed list. **Recommendation (don't act, just surface):** when an agent uses `bundles/AGENTS.template.md` to write a new bundle's docs from scratch in Phase 3, the template's example shapes should be derived from a "freshly-introduced bundle that has no consumers yet" — the plan workflow finding §7 already raises this.
- Pattern-grounded: the template should be writable end-to-end given just the skeleton commit's contents (items.py + metadata.py + files/*); verify by tracing one (`5274639` bootshorn) through the template fields. If any field is unfillable from the artifacts, that's an alignment gap. **Suggest verification step** during PR2.

### Story 9: Onboard a new node

**Pattern.** Create `nodes/<location>.<role>.py`, populate metadata + groups, often touch group files to wire membership. Sometimes accompanies adding a new bundle (Story 8) — but more often the bundles already exist and this is "deploy bundles X, Y, Z to a new machine."

**Frequency.** 10 new nodes in 18 months: home.bootshorn-laptop, home.rack-switch-10g (later renamed), home.switch-rack-poe, home.switch-vorratsraum-poe, home.switch-wohnzimmer-10g, home.wohnzimmer-switch-10g (later renamed/deleted), htz.l4d2.py_ (intentionally non-loaded — see naming), mseibert.mailman, mseibert.yourls, ovh.left4me.

**Files typically touched.**
- Always: `nodes/<x>.py` (new file).
- Often: 1-3 `groups/*.py` (membership lists; or `groups/os/<os>.py` to add the node).
- Sometimes: a new bundle (Story 8 overlap) or a new ssh known-hosts entry (`metadata['known_hosts']`).

**Variations.**
- (a) **New machine, existing bundles.** Fastest. Just node + group entries. E.g. `home.switch-rack-10g`-class introductions paired with `routeros` group additions.
- (b) **New machine, new bundle.** Story 8+9 combined. mseibert.yourls (`aeb0a4f`).
- (c) **Suspended-state node** (e.g. `nodes/htz.l4d2.py_` — appended underscore so the loader doesn't pick it up). Notable convention: loader file-pattern based.

**Evidence.**
- `e99fd4b` (2026-05-10) — add ovh.left4me (also updates 2 existing nodes; 39 lines in the new node file).
- `aeb0a4f` (2025-06-22) — mseibert.yourls (yourls bundle + vhost + node introduced together).
- `5274639` (2025-07-11) — bootshorn-laptop introduction.
- `9a51943` (2025-07-10) — switch-rack-poe.
- `58007f5` (2026-03-07) — `dowsnt exist` adds `nodes/htz.l4d2.py_` (suspend convention).

**Co-modification.** Always cross-area: node + (group or bundle).

**Stakes.** Routine for adding to existing capacity. Moderate when the new node introduces a new role (mailman host, l4d server). High when the node has a typo in its `groups` list — typo silently fails to inherit, which the user explicitly added an error printer for (`dc40295`).

**Implications for agent docs.**
- `nodes/AGENTS.md` covers the eval() mechanism and naming convention.
- **Gap A:** the *suspend* convention (`*.py_` doesn't load) is a real, recurring practice — see `nodes/htz.l4d2.py_`. The spec/plan don't mention it. One line in `nodes/AGENTS.md` "Conventions" section warranted.
- **Gap B:** "first-time node onboarding" sequence isn't a workflow that has docs anywhere. Possibly belongs in `bundles/AGENTS.md` "How to add" cross-linked to `nodes/AGENTS.md`. The plan's workflow validation already added a wiring step for *adding a bundle*; a symmetric "How to add a node" in `nodes/AGENTS.md` would be parallel.
- Verification: `bw nodes`, `bw groups -n <node>`, `bw metadata <node>` — already in `commands.md`. ✅

### Story 10: Group adjustment / new OS variant

**Pattern.** Edit `groups/<area>/<x>.py` (or add a new file there). The "membership" function — which nodes get which bundles, and what default metadata flows. A small but high-leverage area.

**Frequency.** ~12 commits in 18 months. Concentrated in `groups/os/routeros.py` (10 touches — driven by the routeros burst) and the debian-13 family (`groups/os/debian-13-common.py`, `debian-13.py`, `debian-13-pve.py` all introduced 2025-08-09 onwards).

**Files typically touched.**
- Most often a single `groups/os/<os>.py`.
- For OS-version upgrades: 1-2 new files in `groups/os/`, parallel to existing version files.
- Membership edits: occasionally also pull in a node file (paired Story 9).

**Variations.**
- (a) **New OS variant.** debian-13 introductions (`c41e6f8` added `debian-13-common.py`, `debian-13.py` and deleted `debian-11.py`). proxmox-ve added `debian-12-pve.py`.
- (b) **Membership tweak.** `b81c9e9` "allow snmp at home" toggles `groups/locations/home.py`.
- (c) **Per-OS metadata adjustment.** `groups/os/routeros.py` got 10 touches as the routeros bundle matured.

**Evidence.**
- `c41e6f8` (2025-08-09) — debian 13 (introduces `groups/os/debian-13.py`, `debian-13-common.py`; deletes `debian-11.py`).
- `b81c9e9` (2025-12-16) — allow snmp at home (groups/locations/home.py).
- `8d941eb` (2025-06-28) — open fw for iperf (groups/os/debian.py).
- `463cf87` (2025-12-03) — mikrotik more port config (groups/os/routeros.py + 4 switch nodes).

**Co-modification.** Group edits often pull in 2-5 nodes (when adding/removing a group, the affected nodes' files are also adjusted). For new OS variants, add a node group file + bump nodes' `groups` lists + sometimes add a new apt key.

**Stakes.** **High.** A group's membership controls which bundles a node ships with, and metadata flows down via merge order (`all` → location → os → machine → applications → node). Wrong group membership = wrong bundles installed = real-machine consequences.

**Implications for agent docs.**
- `groups/AGENTS.md` covers eval() loading, the subdir convention (`applications/`, `locations/`, `machine/`, `os/`), and `all.py`. ✅
- Inheritance/merge order is in `conventions.md` (planned). ✅
- **Gap A:** the "create a new OS variant" recipe isn't documented. Concrete steps the user followed in `c41e6f8`: (1) add `groups/os/debian-13.py` + `debian-13-common.py`; (2) add `data/apt/keys/debian-13-*.asc`; (3) ensure dependent bundles handle the new os string (e.g. `bundles/bind/items.py` was bumped). Worth a paragraph in `groups/AGENTS.md`.
- **Gap B:** the *family-file pattern* (`debian-13-common.py` shared by `debian-13.py` and `debian-13-pve.py`) — a non-trivial idiom. Not in the spec/plan. One line in `groups/AGENTS.md` Conventions.

### Story 11: Disable temporarily / "for now"

**Pattern.** Comment out or stub out a block of working config to take it offline temporarily — service is broken upstream, host is offline, user is debugging, etc. Marker phrases in the commit message: "for now", "disable", "comment out", "dummy". The changes are not deletions; they're meant to be reversed.

**Frequency.** ~10 commits in 18 months. Recurring enough to be a recognized workflow.

**Files typically touched.** Single file. Usually a node file or a metadata.py.

**Variations.**
- (a) **Disable a node entirely** (e.g. `35243fd` 2025-06-22 "offsitebackup offline"; `4f990f8` 2024-01-08 "stromzaehler is offline for now").
- (b) **Comment out a metadata block** (`bf38520` 2026-03-07 "comment out slow download workshop maps"; `16313b9` 2025-01-09 "disable tasnomta charge"; `4652a42` 2026-01-10 "disable zfs mirror for now").
- (c) **Dummy the role out** (`19a8d28` 2025-07-08 "homeassistant os is dummy"; `c03b033` 2026-05-10 "macbook dummy" — yes, the most recent commit).

**Evidence.**
- `4652a42` (2026-01-10) — disable zfs mirror for now.
- `bf38520` (2026-03-07) — comment out slow download workshop maps.
- `c03b033` (2026-05-10) — macbook dummy (most recent commit, `nodes/macbook.py`).
- `35243fd` (2025-06-22) — offsitebackup offline.
- `4f990f8` (2024-01-08) — stromzaehler is offline for now.

**Co-modification.** None.

**Stakes.** Routine, but **easy for an agent to misread**. Disabled-but-committed code looks broken at first glance. An agent that "fixes" it will undo a deliberate suspension.

**Implications for agent docs.**
- **⚠ Real gap.** Nothing in the planned docs warns an agent about the "for now" idiom. An agent doing a "tidy-up" pass could re-enable a deliberately-disabled node.
- Belongs in `conventions.md` (planned) under a "Patterns to recognize and not break" subsection. One line: "Commits with 'for now' / 'disable' / 'dummy' / 'offline' in the message indicate a deliberate suspension. If you encounter a stub or commented-out block, check `git log -- <file>` for that pattern before re-enabling. The user reverses these manually when ready."
- Verification: `bw nodes` is silent on whether a node *should* be picking up a bundle — there's no signal in tooling. Pure-doc fix.

### Story 12: Cross-bundle metadata-reactor refactor

**Pattern.** A change in *one* bundle's `metadata.py` (its `defaults` dict or a `@metadata_reactor`) that writes into other bundles' namespaces, materially altering many bundles' resolved state at once. Rare but expensive.

**Frequency.** 4 high-impact instances in 18 months.

**Files typically touched.** One bundle's `metadata.py` (the source of the change), plus 5-15 other bundles' `metadata.py` (the consumers being updated to match the new contract).

**Evidence.**
- `4959461` (2026-01-11) — `bundles/telegraf/items.py: use new bundle from isac`. Restructures the entire telegraf metadata namespace; touches **12 bundles** (apcupsd, bind, hardware, postfix, postgresql, raspberry-pi, routeros-monitoring, smartctl, tasmota-charge, telegraf, zfs). 660 lines changed in routeros-monitoring/metadata.py alone.
- `985a15e` (2026-01-11) — `wol waker only allow wakeonlan command`. Touches 8 bundles' metadata + 5 nodes via the wol-waker reactor's contract.
- `186d503` (2026-05-10) — bundlewrap 5 migration. **Cross-cutting** rewrite of "non-reading and KeyError-driven metadata reactors per the bw 4→5 migration guide." 11 bundles + items/download.py.
- `7eac09e` (2025-08-09) — `ovh.secondary cake`. Cross-bundle: linux + network + pppoe metadata + node.

**Co-modification.** Always wide. The change pattern fans out from one bundle to many.

**Stakes.** **Highest blast radius in the repo.** Reactors that write across namespaces are the spec's documented warning case (commands.md side-effect-model paragraph). When such a reactor's contract changes, every consumer must update in lockstep.

**Implications for agent docs.**
- `commands.md` already calls out that `bundles/<x>/metadata.py` changes can ripple — first row of the after-change table says "for all nodes including bundle x" and notes "reactors can ripple beyond x's namespace." ✅
- **⚠ Per-bundle gap.** The agent's signal that *this* bundle is one of the cross-writers should live in the per-bundle `Gotchas` or a `Writes into` section. Currently the per-bundle template (spec §3) has `Depends on` (which other bundles this bundle needs) but **not** `Writes into` (which other bundles' namespaces this one writes via reactor). For telegraf, monitored, archive, wol-waker, apt — that's the most important fact.
- **Recommend (don't act):** consider adding an optional `## Writes into` section to the per-bundle template, or fold this into `Gotchas`. Without it, an agent editing `bundles/telegraf/metadata.py` won't know it's about to ripple unless it reads the diff carefully.
- Bundlewrap 5 migration kind of work is one-shot — not worth a separate doc, but worth a sentence in `conventions.md` noting "this repo is on bundlewrap 5.0.3" so an agent doesn't apply 4.x patterns. Plan already covers this. ✅

### Story 13: Cleanup / delete obsolete code

**Pattern.** Pure-deletion or near-pure-deletion commits that remove dead bundles / nodes / templates. Often follows a Story 5 burst (the burst ended; old artifacts now obsolete).

**Frequency.** ~8 commits in 18 months.

**Files typically touched.**
- Bundle deletions: 3-10 files in `bundles/<x>/`.
- Node deletions: 1 node file.
- Single-file template removals: 1 file.

**Variations.**
- (a) **Remove an obsolete bundle entirely.** `849c305` "remove obsolete homeassistant supervised" deletes 3 files. `ac8e7e2` "delete old l4d bundles" deletes 12 files across left4dead2_old, left4dead2_old2, left4dead2_steam_old.
- (b) **Remove an obsolete node.** `e65aa8f` deletes `nodes/home.openhab.py`. `c41e6f8` deletes `nodes/htz.games.py`.
- (c) **Remove a single dead artifact.** `2899cd5` deletes `bundles/nextcloud/files/rescan`. `32ea52c` deletes `bundles/mariadb/files/override.conf`.

**Evidence.**
- `ac8e7e2` (2026-02-10) — delete old l4d bundles (12 files deleted, 0 added).
- `849c305` (2025-07-13) — remove obsolete homeassistant supervised.
- `800bd90` (2025-06-28) — remove apcupsd.
- `e65aa8f` (2025-08-09) — openhab no longer exists.

**Co-modification.** Sometimes nudges nodes that referenced the deleted bundle (e.g. `e65aa8f` also edits home.server.py to remove the openhab include). Pure-deletion if the bundle was already orphaned.

**Stakes.** Low when the asset is truly orphaned. Moderate if a node still references the deleted bundle (silent failure mode: bw will complain at apply time). **The user's workflow is: delete → next bw command surfaces dangling refs → fix.**

**Implications for agent docs.**
- `bundles/AGENTS.md` "How to add" exists; **no symmetric "How to remove"** — and the recurring pattern is real. Worth a 5-line section: "To remove a bundle: (1) `git grep '<name>'` to find references in nodes/groups/other bundles; (2) remove those references; (3) `rm -rf bundles/<x>/`; (4) `bw test` and `bw nodes` to confirm clean."
- Verification command sequence is in `commands.md`. ✅

### Story 14: Add or revise an operator script (`bin/`)

**Pattern.** Either introduce a new `bin/<script>` (one-off operator tooling, not invoked by bundlewrap) or revise an existing one. Standalone — usually does not pair with bundle changes.

**Frequency.** ~8 commits in 18 months. 4 new scripts: `bin/passwords-for`, `bin/sync_1password`, `bin/timestamp_icloud_photos_for_nextcloud`, `bin/mikrotik-firmware-updater`.

**Files typically touched.** Single `bin/<script>` file.

**Variations.**
- (a) **Introduce new script** (commit subject often includes ": introduce").
- (b) **Refactor existing script** — `bin/wireguard-client-config` was renamed from `bin/wireguard_client_config` in `1f4aaad` and the same commit improved it.
- (c) **Bug fix.** `dcd2ebc` "dist-upgrade -> full-upgrade" in `bin/upgrade_and_restart_all`.

**Evidence.**
- `60c2c42` (2026-03-09) — `bin/timestamp_icloud_photos_for_nextcloud: introduce`.
- `979c7e1` (2025-12-03) — `bin/passwords-for: introduce`.
- `2b873e4` (2025-12-01) — `bin/sync_1password` (script for syncing routeros logins to 1password).
- `86d9b8b` (2025-12-13) — `bin/mikrotik-firmware-updater` introduced (alongside `libs/version.py`).
- `fe5e340` (2025-12-03) — `bin/script_template: repo -> bw` (the user keeps a template script for new bin scripts).

**Co-modification.** `86d9b8b` paired with `libs/version.py` (script-needs-helper pattern). Otherwise standalone.

**Stakes.** Low. Operator scripts run on demand by the user, not automatically.

**Implications for agent docs.**
- `bin/AGENTS.md` (planned) covers what bin/ is for. ✅
- The existence of `bin/script_template` is itself a useful convention — an agent should start a new bin script from this template. **⚠ Mention it explicitly** in `bin/AGENTS.md` "How to add" — currently not in spec.
- Plan PR1 step 7 adds `# purpose:` headers to bin scripts. The existing scripts use varied conventions — verify the header pass actually achieves uniformity. ✅

### Story 15: OS-version upgrade campaign

**Pattern.** Move nodes from one Debian major to the next. A long-tail campaign (per-node, weeks apart) rather than a single commit. Touches: new `groups/os/debian-N*.py`, new apt keys in `data/apt/keys/`, per-bundle adjustments where the new OS shipped with different packages or service names.

**Frequency.** 3 campaigns in the visible history: debian-12 (Jul 2023, ~10 commits), debian-13 (Aug 2025, ~15 commits), trixie-on-server-only (Mar 2026, 1 commit so far — early).

**Files typically touched (per campaign).**
- New: `groups/os/debian-N*.py`, `data/apt/keys/debian-N-*.{asc,gpg}`, potentially `data/apt/keys/proxmox-ve-N.gpg`.
- Modified: per-bundle metadata to handle new OS string; nodes' `groups` lists bumped.
- Deleted: old OS group file (`groups/os/debian-11.py` deleted in debian-13 campaign; old keys retained as `_.asc` for ref).

**Evidence.**
- `c41e6f8` (2025-08-09) — debian 13 (campaign seed: introduces debian-13 group files, adds apt keys, adjusts bind, removes debian-11 group, removes htz.games node).
- `9621184` (2025-08-10) — htz.mails debian 13 (per-node bump + dovecot/redis/roundcube/systemd-swap adjustments).
- `bc656cd` (2025-08-09) — backups debian 13 (one-line node bump).
- `cb19c38` (2026-03-07) — update home.server to trixie (campaign seed for the next round; touches proxmox-ve metadata, ssh items, debian-13 keys/groups, multiple nodes).

**Co-modification.** Wide: data/ + groups/ + bundles/ + nodes/ in one commit each campaign-step.

**Stakes.** **High.** Each step touches a real machine; failures are recovery work. The user has been bitten — `c41e6f8` deleted `htz.games.py` outright, suggesting that node was decommissioned alongside its OS.

**Implications for agent docs.**
- `conventions.md` (planned) mentions group inheritance order. ✅
- **Gap.** The "campaign" workflow itself isn't documented anywhere. An agent helping with an OS bump won't know whether to (a) start a new `groups/os/debian-N*.py` family or (b) edit the existing one. The user's pattern is consistent: parallel new files, swap node memberships gradually, delete the old when no consumers remain.
- Worth a few lines in `groups/AGENTS.md` "How to add / modify": "When introducing a new OS major, mirror the existing `debian-N-common.py` + `debian-N.py` + `debian-N-pve.py` triad and bump nodes one at a time. Don't edit the old OS file in place — let it die when no nodes reference it."
- Verification: pre-bump `bw hash <node>` vs post-bump diff (planned). ✅

### Story 16: Add or modify a lib

**Pattern.** Edit `libs/<x>.py` (a Python module importable from bundles via `repo.libs.<x>`) or add a new lib. The widest blast radius in the repo — every bundle that imports the lib re-evaluates on next apply.

**Frequency.** 5 commits over 18 months. 1 new lib (`libs/version.py` in `86d9b8b`).

**Files typically touched.**
- Single `libs/<x>.py` for tweaks.
- Sometimes paired: `requirements.txt` if a new dependency is needed (`1d8361c` 2025-06-22 changed `libs/rsa.py` and `requirements.txt` together: `cache_to_disk broken`).

**Evidence.**
- `86d9b8b` (2025-12-13) — `libs/version.py` introduced (mikrotik-firmware-updater needs version compare).
- `1d8361c` (2025-06-22) — `libs/rsa.py` cache_to_disk broken.
- `32ea52c` (2025-06-27) — `libs/ini.py` modified (mariadb refactor uses ini parser).
- `e486aad` (2025-12-13) — `libs/bind.py` whitespace.

**Co-modification.** Rare. Lib changes don't pull in their consumers unless the lib's API changed.

**Stakes.** **Highest blast radius among non-reactor changes.** All bundles that import the lib re-evaluate; all nodes that include those bundles see the effect.

**Implications for agent docs.**
- `libs/AGENTS.md` (planned) covers the convention. ✅
- `commands.md` already says `libs/<x>.py` change → `bw hash` all nodes. ✅
- Plan PR1 step 7 adds module docstrings to libs. ✅ (Critical here — without a one-line docstring, the agent has to read the body to know what the lib does, defeating discovery-by-`ls`.)
- **Gap (minor).** The plan doesn't mention checking which bundles import a given lib — an agent making a breaking change to `libs/hashable.py` should know who imports it. `git grep -l 'repo.libs.hashable'` is a one-line snippet that could live in `libs/AGENTS.md` "Pitfalls."

### Story 17: Add or modify a hook

**Pattern.** Edit `hooks/<x>.py` (lifecycle hook fired by bw on specific events, e.g. before-apply, after-test). Like libs, repo-wide blast radius — a hook fires for *every* bw command of the right kind.

**Frequency.** 4 commits in 18 months. 2 new hooks.

**Files typically touched.** Single hook file. Sometimes paired with the bundle whose data the hook reads.

**Evidence.**
- `0603a8c` (2025-12-01) — `hooks/unique_node_ids.py: introduce` (a `bw test`-time uniqueness check).
- `7ea760d` (2026-01-11) — `hooks/test_ptr_records.py: introduce` (paired with mailserver metadata edit).
- `7f43efc` (2025-12-03) — `hooks/wake_on_lan.py: dedup` (refactor existing hook).

**Co-modification.** Sparse. The new ptr-records test hook also touched `bundles/mailserver/metadata.py` because the hook reads from there.

**Stakes.** **High.** A broken hook breaks every bw command that fires it — an agent can't even run `bw test` to see what's wrong if the hook errors at hook-load time. Recovery requires either fixing the hook or `git stash`.

**Implications for agent docs.**
- `hooks/AGENTS.md` (planned) covers the bw hook lifecycle and how to write one. ✅
- Plan PR1 step 7 adds module docstrings. ✅
- **⚠ Gap.** The "broken hook breaks all bw commands" failure mode isn't documented. An agent introducing a hook should test it in isolation first (e.g. import the module in `bw debug`) before letting it run in `bw test`. Worth one paragraph in `hooks/AGENTS.md` "Pitfalls."

### Story 18: Per-bundle README touch-up

**Pattern.** Edit `bundles/<x>/README.md` — sporadic, prose-only, usually adding a note to a bundle the user wants to remember something about. ~33 bundles currently have READMEs (more than the spec's "~10 of 103" estimate).

**Frequency.** ~8 commits in 18 months. mailman (`9bbaeb6`, `7df2187`, `980fdc8`), freescout (`64029d2`, `8081f12`, `4ec2d51`), l4d2 (`a397399`, `278f6de`), apt (`3dffc05`).

**Files typically touched.** Single README.

**Evidence.**
- `9bbaeb6` (2025-07-12) — mailman poc email sent (creates README and tests).
- `64029d2` (2024-11-23) — freescout readme.
- `a397399` (2026-02-10) — l4d readme.

**Co-modification.** Sometimes paired with code changes in the same bundle.

**Stakes.** Routine.

**Implications for agent docs.**
- **Big alignment issue.** PR2 plan replaces existing per-bundle READMEs with `AGENTS.md` for the 10 seed bundles. The plan correctly notes "verify with `find bundles -name README.md`" — actual count is **33 READMEs**, not the ~10 in the plan's table. The seed list intersects only minimally with the README list:
  - On both lists (seed + has README): nextcloud, telegraf, apt, mariadb (note: mariadb isn't on the seed list, but has README), letsencrypt.
  - Seed-list bundles **without** existing READMEs: monitored, postgresql, wireguard, php, nginx, backup. (Verified by `find bundles -name README.md`.)
  - READMEs on bundles **not** in seed list: ~25, including freescout, mailman, mailserver, mariadb, dm-crypt, dovecot, nodejs, nginx-rtmps, nftables, smartctl, wol-sleeper, wordpress, archive, gcloud, grafana, icingaweb2, influxdb2, raspberrymatic-cert, routeros, systemd, systemd-timers, tasmota-charge, telegraf, zfs, build-server, apcupsd, flask.
- **Recommendation (don't act, just surface):** Phase 3 ("leave-as-you-go") will pick these up over time. **But:** the Phase 1/2 plan should mention that 23 existing READMEs will *remain* (untouched, parallel to AGENTS.md as PR2 only addresses seeds). Eventually those will need folding too. Worth being explicit in the plan that this is a known asymmetry, since `find bundles -name README.md` will report 23 left after PR2 — verifiers will trip on this.
- For agents: `bundles/AGENTS.md` should mention "if a bundle has both a `README.md` and an `AGENTS.md`, the `AGENTS.md` is canonical; the `README.md` is being phased out." Currently planned doc is silent on the transition state.

### Story 19: Naming-convention rename

**Pattern.** Rename a node/bundle/file from underscore-style (or otherwise-irregular) to the canonical lowercase-hyphenated style. Done sporadically as the user notices inconsistency.

**Frequency.** 4 renames in 18 months (excluding internal moves like the mikrotik.mib relocation).

**Evidence.**
- `1f4aaad` (2025-12-16) — `bin/wireguard_client_config` → `bin/wireguard-client-config` (and improved the script in the same commit).
- `d54eff3` (2025-06-30) — `nodes/home.rack-switch-10g.py` → `nodes/home.switch-rack-10g.py` (puts "switch" before location-detail per `<location>.<role>.py`).
- `d54eff3` — `nodes/home.wohnzimmer-switch-10g.py` → renamed in same commit (deleted in subsequent rename to switch-wohnzimmer-10g format).
- `f0d1cf9` (2024-11-23) — `data/apt/keys/icinga.asc` → `data/apt/keys/icinga_.asc` (here the rename adds an underscore, but it's actually a "park the old file" pattern so the user can replace with a new gpg).
- `78a8abc` (2025-12-16) — `data/routeros-monitoring/files/mikrotik.mib` → `bundles/routeros-monitoring/files/mikrotik.mib` (move from `data/` into the bundle — *relocation* convention, see cross-cutting findings).

**Files typically touched.** 1-2 paths (the rename), plus often 1-3 references in other files (groups, nodes).

**Co-modification.** The wireguard rename in `1f4aaad` was paired with script changes ("improve wireguard config gen"); the switch renames in `d54eff3` paired with the routeros bundle work.

**Stakes.** Low individually but **silent-trap-prone**: a rename of a node file changes the node's identity (since the loader file-name → node-name). Anything keyed by node name (vault entries via `!password_for:<node>`, hash records, ssh known_hosts) needs a parallel rename or the node loses its associations.

**Implications for agent docs.**
- The plan's workflow validation finding §4 already calls for documenting the bundle naming convention (lowercase-hyphenated, no underscores). ✅
- **Gap.** The node rename failure-mode isn't documented. Agents may rename a node file thinking it's purely cosmetic. One sentence in `nodes/AGENTS.md` Pitfalls: "Renaming a node file renames the node. `!password_for:<old-name>` magic strings, vault entries, and known_hosts associations all key on node name — search and replace before renaming."

### Story 20: Bundlewrap version migration (one-shot)

**Pattern.** Migrating the repo from one major version of bundlewrap to the next. Has happened once in the visible history (4.x → 5.0.3 in `186d503` on 2026-05-10) and is uniquely high-stakes.

**Frequency.** 1 commit in 18 months — but the maintainer is, per the handoff context, also planning to design their own config-management tool, so **this story is effectively an N=1 sample of "language migrations" the maintainer cares about.**

**Files touched.** 13 files: 11 `bundles/<x>/metadata.py`, `items/download.py`, `requirements.txt`. Per the commit body: rewrites "non-reading and KeyError-driven metadata reactors" per the bw 4→5 migration guide; renames custom Download item methods (`cdict/sdict/get_auto_deps` → `expected_state/actual_state/get_auto_attrs`).

**Evidence.** `186d503` (2026-05-10).

**Co-modification.** Wide cross-bundle. Mixes Story 12 (cross-bundle reactor) with Story 6 (items.py interface) into one operation.

**Stakes.** Highest. Rewriting reactors and item-type interfaces simultaneously means the repo is broken until the last file is corrected.

**Implications for agent docs.**
- `conventions.md` (planned) notes the bundlewrap version. ✅
- `commands.md` notes `requirements.txt` is the version pin. ✅
- **Gap.** The migration was done with Claude assistance (per the commit's `Co-Authored-By`). An agent helping with the *next* major migration would benefit from a one-paragraph "how to do a bw version migration" recipe in `conventions.md`: read upstream migration guide → list affected reactor patterns → grep for them → rewrite each → bump `requirements.txt` last. **Recommendation (don't act):** worth capturing as a section in conventions, given the maintainer's own tool-design plans suggest such migrations will recur.

### Story 21: Interactive `bw debug` investigation

**Pattern.** Open `bw debug` (the bundlewrap interactive Python REPL with `repo` and `bw` preloaded), explore the repo state, prototype a code snippet. The 15-line `.bw_debug_history` is short but representative of how the user investigates before changing.

**Frequency.** Hard to count from git (history file is gitignored as of `39d5fb8` 2025-10-28). Evidence in-tree is one persistent file with 15 unique lines.

**What's in `.bw_debug_history`:**
```
bw.get_node('home.switch-wohnzimmer-10g')
repo.get_node('home.switch-wohnzimmer-10g')
repo.get_node('home.switch-wohnzimmer-10g').password
from os import path, listdir
path.join(repo.path, 'bundles/left4dead2/files/scripts/overlays')
listdir(path.join(repo.path, 'bundles/left4dead2/files/scripts/overlays'))
listdir(path.join(repo.path, 'bundles/left4dead2/files/scripts/overlays'))[0]
listdir(path.join(repo.path, 'bundles/left4dead2/files/scripts/overlays'))
from os import path, listdir
a = listdir(path.join(repo.path, 'bundles/left4dead2/files/scripts/overlays'))[1]
a
type(a)
repo.libs.ovh
type(a)
repo.libs.ovh
```

**What this reveals.** The user (a) treats `bw debug` as a Python REPL with `repo`/`bw` pre-bound; (b) inspects nodes by name; (c) walks the filesystem inside `bundles/<x>/files/<dir>/` (the l4d overlay scripts work from Story 5); (d) probes `repo.libs.<name>` to see what's available — the trailing `repo.libs.ovh` looked up an ovh helper. This is **dynamic discovery**, complementary to file reads.

**Stakes.** Read-only — `bw debug` doesn't apply state. Routine.

**Implications for agent docs.**
- `commands.md` lists `bw debug` as read-only. ✅
- **⚠ Gap.** The *content* of `bw debug` (what's in scope: `repo`, `bw`, `node = repo.get_node(...)`, `node.metadata`, `repo.libs.<x>`) isn't sketched in `commands.md`. An agent that wants to investigate dynamically won't know what to type. One paragraph + 5 example lines (drawn directly from `.bw_debug_history`) would suffice.
- Mention the gitignore: `.bw_debug_history` is gitignored (as of `39d5fb8`), so an agent's debug session won't accidentally land in a commit. Already covered by spec §4 quickstart's "do not modify" list. ✅

## Cross-cutting findings

### F1. Commit-message style is terse, iterative, and unreliable
First-word frequency: `l4d` (22), `fix` (18), `bootshorn` (8), `routeros` (6), `remove` (6), `update` (4), `more` (4), `add` (4). Many subjects are typos (`fixmo`, `besteffort`, `dowsnt exist`, `mroe`, `unfault`, `englisch sprache schwere sprache`). The terseness is feature, not bug — see Story 4 (microbursts as workflow). Conclusion: **agents must read diffs, not subjects.** The detailed-history extraction approach (`git log --name-status -M -C`) was load-bearing; subject-only clustering would have over-bucketed.

### F2. The "introduce" verb is a reliable seed marker
When the user names a commit `<path>: introduce` (or `<path>: introduce + …`), it's almost always the seed of a new bundle/script/hook/node skeleton. ~7 such commits in 18 months. Not a story per se, but a useful corpus marker for "where did X come from."

### F3. Naming convention: lowercase-hyphenated
Confirmed across the bundle list — every current bundle uses lowercase-hyphenated naming (e.g. `backup-server`, `bind-acme`, `dm-crypt`, `homeassistant-supervised`, `kea-dhcpd`, `mailserver-autoconfig`, `nginx-rtmps`, `nextcloud-picsort`, `proxmox-ve`, `raspberry-pi`, `raspberrymatic-cert`, `routeros-monitoring`, `systemd-networkd`, `systemd-swap`, `systemd-timers`, `tasmota-charge`, `wol-sleeper`, `wol-waker`, `zfs-mirror`). The few underscore-named bundles (`left4dead2_old`, `left4dead2_old2`, `left4dead2_steam_old`) were all deleted via `ac8e7e2`. Bin scripts mostly hyphenated (after `1f4aaad` rename) but **a handful still underscored** (`bin/sync_1password`, `bin/timestamp_icloud_photos_for_nextcloud`, `bin/upgrade_and_restart_all`, `bin/script_template`, `bin/passwords-for`). Verdict: **convention is hyphenated, but underscored exceptions exist in `bin/`.** An agent should normalize to hyphenated for new bundles/nodes; for `bin/`, match the user's existing style (mixed).

### F4. Subdirectory-relocation pattern in active bundles
`78a8abc` moved `data/routeros-monitoring/files/mikrotik.mib` into `bundles/routeros-monitoring/files/mikrotik.mib`, with the commit message "move to bundle bc why not." This was a *consolidation* — pulling bundle-specific data from `data/` into the bundle itself. Single instance, not yet a strong story, but suggests the user's mental model is `data/` = "shared/templated artifacts read by multiple bundles", `bundles/<x>/files/` = "this bundle's static files." Worth a sentence in `data/AGENTS.md`: "if a data asset is read by exactly one bundle, prefer placing it in `bundles/<x>/files/`."

### F5. Bursts have a characteristic shape
Pattern observed in all 5 bursts: (i) seed commit introduces the skeleton in 1-3 hours of intense work; (ii) 1-2 day cooling period; (iii) 2-6 weeks of follow-up commits with shrinking commit-size; (iv) often a "delete obsolete" cleanup commit (Story 13) at the end. l4d2 followed this shape exactly (seed `3469d98` Aug 24, refinement Aug-Feb, cleanup `ac8e7e2` Feb 10). Recognizable signature for an agent reading recent history: many commits to one area in N days = active subsystem.

### F6. `_old` and `_old2` as a "soft delete" pattern
The l4d2 rebuild renamed working code into `bundles/left4dead2_old/` and `bundles/left4dead2_old2/` (commit `3469d98`) before later deletion in `ac8e7e2`. The user uses suffixed-with-`_old` directories as a recovery buffer during big refactors. **Agents shouldn't delete `_old`/`_old2`-suffixed bundles without checking with the user**; they may be deliberate parking spots. Currently there are none in-tree (the `delete old l4d bundles` cleanup landed), but the pattern will recur.

### F7. The repo has no test suite, no CI, no formal type annotations
Confirmed by tree inspection and history. The verification model is `bw test` (loader sanity), `bw hash` (state diff), `bw verify` (drift check) — a runtime check, not a static one. This shapes agent expectations: **don't propose test additions or CI without explicit user request** (the spec's "no tooling changes" non-goal aligns). Agents should use `bw debug` for ad-hoc validation instead of writing fixtures.

### F8. Merge commits are real, but bursts are usually merged via squash
PRs visible in the history: `#18` homeassistant-supervised, `#19` mseibert_yourls, `#22` proxmox_mergable, `#23` routeros, `#24` ipv6_picking, `#25` debian-13, `#26` htz.mails_debian_13_squash, `#27` l4d2_the_next. The user uses Gitea/Forgejo for PRs (self-hosted). Naming pattern: descriptive branch name → PR. For agents creating PRs in this repo, branch-name style: lowercase-snake_case description (mirrors PR titles).

### F9. The README.md is a personal TODO, not a project README
First lines of `README.md`: `# TODO\n\n- dont spamfilter forwarded mails\n- gollum wiki\n- blog?`. Already noted in spec §1 ("untouched personal TODO list") and plan PR1 step 8. **Agents must not regard the root README as documentation for the repo.** Unique enough to merit explicit callout in root `AGENTS.md`: "Note: `README.md` is the maintainer's personal scratchpad. Real onboarding lives here." Spec §4 and plan don't currently include that exact callout.

### F10. Commit cadence is bursty across years, not just months
Total commits since first commit (2021-06-11): 1169. Last 36 months: 343. Last 24 months: 251. Last 18 months: 222. Last 12 months: 158. So ~70% of commits are in the last 24 months, but only ~10% in the last 12 months — meaning **commit activity has been declining**. Agents reading "recent history" should weight 6-12 months heavier than 12-24 months for "current state." (One nuance: the very last burst — May 2026 bundlewrap-5 migration — is recent, suggesting renewed activity ahead of the planned tool-design pivot.)

## Story coverage assessment vs the planned docs

For each story, traffic-light against PR1+PR2 as currently planned (root `AGENTS.md`, 8 area docs, conventions.md, commands.md, per-bundle template, 10 seed per-bundle docs, docstring/header pass on libs/hooks/bin, fork's `AGENTS.md` for bundlewrap language).

| # | Story | Status | Justification |
|---|---|---|---|
| 1 | Tune one bundle's metadata | ✅ | Per-bundle `Metadata` section; `commands.md` after-change row; mostly works as planned. |
| 2 | Tweak one node's config | ⚠ | `nodes/AGENTS.md` covers eval() but should explicitly add the silent-load-failure pitfall (the user himself patched the loader for this — `dc40295`). |
| 3 | Edit a file template | ⚠ | `bundles/AGENTS.md` lists `files/` in anatomy, but doesn't document Mako-vs-static recognition. Plan workflow finding §5 already adds the link to the fork's template guide — likely sufficient when written. |
| 4 | Trial-and-error microburst | ❌ | Workflow-style context not captured anywhere. Belongs in root `AGENTS.md` quickstart or `conventions.md`: "user's commits are iterative; don't rebase WIP without asking." |
| 5 | Subsystem deep-dive burst | ❌ | "Hot subsystem" awareness not in any planned doc. Seed bundle list (Phase 2) misses 3 of 5 recent burst targets (routeros, routeros-monitoring, bootshorn). Recommend rebalancing or documenting how to detect flux. |
| 6 | Modify items.py for a bundle | ✅ | `bundles/AGENTS.md` + fork's items reference covers item types & deps. Item `download.py` docstring (PR1 step 7) closes the custom-item gap when written. |
| 7 | Templated data update | ⚠ | `data/AGENTS.md` will exist; needs to distinguish apt-keys-as-data vs grafana-rows-as-Python. After-change check for apt keys not explicit in `commands.md`'s table — a one-line addition. |
| 8 | Add a new bundle | ✅ | Per-bundle template + spec §3 is well-shaped. Plan workflow finding §3 added explicit wiring step. ✅ |
| 9 | Onboard a new node | ⚠ | `nodes/AGENTS.md` covers eval() & naming, but missing: (a) the `*.py_` suspend convention; (b) symmetric "How to add a node" workflow paragraph. Both are one-line fixes. |
| 10 | Group adjustment / new OS variant | ⚠ | `groups/AGENTS.md` covers basics; missing the family-file pattern (`debian-N-common.py` shared by `debian-N.py` + `debian-N-pve.py`) and the new-OS recipe. Both are paragraph-sized adds. |
| 11 | Disable temporarily / "for now" | ❌ | Not in any planned doc. Real risk: agents "fixing" deliberately-stubbed code. Belongs in `conventions.md` as a single paragraph. |
| 12 | Cross-bundle metadata-reactor refactor | ⚠ | `commands.md` warns about cross-namespace ripple in general. Per-bundle template lacks a `Writes into` field — recommend adding it (or folding into `Gotchas`) for cross-writing bundles (telegraf, monitored, archive, wol-waker, apt). |
| 13 | Cleanup / delete obsolete code | ⚠ | "How to remove a bundle" not in `bundles/AGENTS.md`. Symmetric to "How to add" — 5-line addition. |
| 14 | Add or revise an operator script (`bin/`) | ⚠ | `bin/AGENTS.md` covers what bin/ is; missing mention of `bin/script_template` as the canonical starter. One-line. |
| 15 | OS-version upgrade campaign | ⚠ | Inheritance order in `conventions.md`; no campaign recipe. Belongs in `groups/AGENTS.md` "How to add" — paragraph-sized. |
| 16 | Add or modify a lib | ✅ | `libs/AGENTS.md` + docstring pass + `commands.md` blast-radius row. Could optionally add a "find consumers" snippet (`git grep`). Minor. |
| 17 | Add or modify a hook | ⚠ | `hooks/AGENTS.md` covers lifecycle; missing the "broken hook breaks all bw commands" failure-mode and isolation-test recipe. One paragraph. |
| 18 | Per-bundle README touch-up | ⚠ | Plan undercounts existing READMEs (10 → actual 33). PR2 only addresses seed bundles; ~23 READMEs survive. Plan should acknowledge the transition state, and `bundles/AGENTS.md` should note "if both exist, AGENTS.md is canonical." |
| 19 | Naming-convention rename | ⚠ | Plan workflow finding §4 covers bundle naming. Missing: node-rename failure mode (renaming changes node identity, breaks vault keys). Sentence in `nodes/AGENTS.md`. |
| 20 | Bundlewrap version migration | ✅ | One-shot; `conventions.md` will note version. Optional: paragraph in `conventions.md` capturing the migration recipe — useful given maintainer's tool-design pivot. |
| 21 | Interactive `bw debug` investigation | ⚠ | `commands.md` lists `bw debug` as read-only. Missing: what's in scope inside `bw debug` (paragraph + 5 example lines pulled from `.bw_debug_history`). |

**Tally.** ✅ 5 / ⚠ 13 / ❌ 3.

The ❌ gaps (S4 trial-and-error workflow context, S5 burst-state awareness, S11 disable-for-now idiom) are the highest-value adds because they shape an agent's *judgment*, not just its lookup steps. The ⚠ gaps are mostly one-line / one-paragraph additions to area docs that are already in scope for PR1.

The Phase 2 seed list is the largest single open question raised by this analysis: it leans toward usage-frequency hubs (postgresql, wireguard, php, nginx) but underweights currently-hot subsystems (routeros, routeros-monitoring, bootshorn). A swap of 2-3 entries — e.g. `php` → `routeros` and `apt` → `bootshorn` — would better match the work the maintainer (and any helper agent) will actually be doing in the next quarter. This is for human decision; not acted on.
