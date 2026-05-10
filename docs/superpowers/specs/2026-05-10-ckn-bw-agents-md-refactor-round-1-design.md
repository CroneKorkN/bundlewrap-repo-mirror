# Round 1 — agent-doc refactor (gaps 1–6 + cmd cheat sheet)

## Why

A previous session integrated `bundles/left4me/` and brought
`ovh.left4me` live. The integration produced a handoff (at
`~/.claude/plans/2026-05-10-ckn-bw-docs-improvements-handoff.md`)
listing 12 documentation gaps surfaced by the work. This spec covers
the first six (the cross-cutting ones) plus a useful side-quest:
adding a read-only command cheat sheet to `docs/agents/commands.md`.
Gaps 7–12 (item-specific, bundle READMEs) are deferred to a follow-up
round.

## Scope

In:

- Gap 1 — drop `bw bundles` (doesn't exist), add `bw verify` to the
  read-only allowlist.
- Gap 2 — bundle-validation workflow needs a node attached.
- Gap 3 — nodes carry only node-specific metadata (split across
  `bundles/AGENTS.md` and `nodes/AGENTS.md`).
- Gap 4 — reactors must read metadata or be defaults.
- Gap 5 — `triggers` ↔ `triggered: True` invariant + self-healing
  pattern.
- Gap 6 — `unless` semantics (folded into Gap 5's second bullet).
- Side-quest: read-only command cheat sheet in `commands.md` (`bw
  test` flag matrix + selectors, `bw metadata -k/-b/-f`, `bw items
  --blame/-f`, `bw verify -o bundle:`, `bw hash -m/-d`).

Out:

- Gaps 7–12 (`source` implicit, `git_deploy` chown, `git_deploy` URL
  form, letsencrypt/bind/nginx READMEs).
- Any change to bundle behaviour. This is pure docs; if a doc claim
  feels wrong, push back to the maintainer rather than editing
  `.py`.

## Verification approach

For each gap, find current line numbers in the target doc (handoff
line numbers are May 2026; some have drifted). Verify code-level
claims against the fork source under `.venv/src/bundlewrap/` before
quoting them.

Already verified during brainstorm:

- Gap 1: `bw bundles` is not a subcommand of the installed fork
  (`.venv/bin/bw --help` lists only
  `apply, debug, diff, groups, hash, ipmi, items, lock, metadata,
  nodes, plot, pw, repo, run, stats, test, verify, zen`). `bw verify`
  is read-only.
- Gap 2: `bw test` default flag set differs by mode. Whole-repo:
  `-HIJKMSp`. Node-targeted: `-IJKMp`. The repo-mode adds `-H`
  (repo hooks) and `-S` (subgroup-loops); the node-mode adds `-J`
  (node hooks). Reactors only resolve when a node's metadata is
  built, which only happens when a node opts into the bundle.
- Gap 4: exact wording at `metagen.py:428`:
  `"{reactor_name} on {node_name} did not request any metadata, you
  might want to use defaults instead"`.
- Gap 5: exact wording at `deps.py:340`:
  `"'{item1}' in bundle '{bundle1}' triggered by '{item2}' in bundle
  '{bundle2}', but missing 'triggered' attribute"`.
- Gap 3 precedent: `bundles/left4me/metadata.py:10` is the canonical
  random-bytes-in-defaults example. `bundles/postgresql/metadata.py:4`
  is the password_for-at-module-scope example. (The handoff cites
  postgresql for the random-bytes pattern; that's a misattribution —
  postgresql uses `password_for`.)

After every commit: `.venv/bin/bw test` must pass with the same
output as before. Pure-docs edits cannot break it unless a `.py` is
touched accidentally.

## Commits

Six iterative commits, matching repo style.

### Commit 1 — drop `bw bundles`, add `bw verify` (Gap 1)

`AGENTS.md` rule 1 only. The handoff also flagged
`bundles/AGENTS.md:60-64`, but that list no longer references
`bw bundles` (it currently reads `bw test` / `bw items` / `bw hash`).
That section gets rewritten in commit 3, not here.

```diff
- to `bw test`, `bw nodes`, `bw groups`, `bw bundles`,
- `bw items`, `bw metadata`, `bw hash`, `bw debug`. See
+ to `bw test`, `bw nodes`, `bw groups`, `bw items`,
+ `bw metadata`, `bw hash`, `bw verify`, `bw debug`. See
```

### Commit 2 — read-only command cheat sheet

Append to `docs/agents/commands.md`. New H2 section, table format
to match the existing voice.

```markdown
## Read-only commands — useful flag combinations

The fork's [`AGENTS.md`][fork] documents the canonical safety envelope.
These are the flag combinations agents reach for most often in this repo:

| Want to … | Run |
|---|---|
| Sanity-check the whole repo (parse + cross-cutting hooks)        | `bw test` (defaults to `-HIJKMSp`) |
| Exercise reactors and item-graph for one node                    | `bw test <node>` (defaults to `-IJKMp`) |
| Same, but every node that has a given bundle                     | `bw test bundle:<name>` |
| Print one metadata key for one node                              | `bw metadata <node> -k <a/b>` (repeat `-k` for more) |
| Show where each metadata value comes from                        | `bw metadata <node> -b` |
| Resolve Faults (vault values) into the dump                      | `bw metadata <node> -f` — **may print secrets, avoid** |
| List a node's items, with the bundle that defines each           | `bw items <node> --blame` |
| Preview a rendered file's content                                | `bw items <node> file:<path> -f` |
| Verify against the live host, scoped to one bundle               | `bw verify <node> -o bundle:<name>` |
| Hash metadata only (faster than full config hash)                | `bw hash <node> -m` |
| Inspect the data backing a hash                                  | `bw hash <node> -d` |

`bw test`, `bw verify`, `bw nodes`, `bw metadata` all share a target-
selector grammar: bare node name, group name, `bundle:<name>`,
`!bundle:<name>`, or `"lambda:node.metadata_get('foo/bar', 0) < 3"`.

[fork]: https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md
```

### Commit 3 — bundle validation needs a node attached (Gap 2)

Two file changes.

**`bundles/AGENTS.md` lines 59-64** — replace the Verify list:

```markdown
5. **Verify, in this order:**
   - `bw test` — repo-wide parse + cross-cutting hooks. Loads every
     bundle, but reactors don't fire for nodes that haven't opted into
     the bundle yet — bugs in new reactors stay hidden here.
   - **Attach the bundle to a node** (via the node's `bundles` list, or
     a group it belongs to). Until you do, the next steps don't actually
     exercise the bundle.
   - `bw test <node>` — exercises every reactor and item-graph edge for
     that node. This is where most new-bundle bugs surface.
   - `bw items <node> --blame` — confirm items materialise with the right
     paths, authored by the expected bundle.
   - `bw metadata <node> -k <a/b>` — spot-check derived metadata.
   - `bw hash <node>` — preview vs current host state.

   See [`docs/agents/commands.md#bundle-validation-workflow`](../docs/agents/commands.md#bundle-validation-workflow)
   for the rationale.
```

**`docs/agents/commands.md`** — new section after the cheat sheet:

```markdown
## Bundle-validation workflow

`bw test` (no args) is a *parsing* gate, not a *behaviour* gate. It
loads every bundle, but a bundle's reactors only resolve when a node's
metadata is actually built — and that happens only for nodes that
opt in. Until then, reactor bugs stay dormant. bw rejects reactors that
don't read any metadata, but the rejection only fires once *some* node
consumes the bundle.

When developing a new bundle:

1. Scaffold + `bw test` — confirms parsing.
2. **Attach the bundle to one node** (or a stub node) by adding it to
   `nodes/<n>.py`'s `bundles` list, or to a group the node is in.
3. `bw test <node>` — now reactors fire. This is where bundle bugs
   surface.
4. `bw items <node> --blame` and `bw metadata <node> -k <key>` — confirm
   items materialise and derived metadata looks right.
5. `bw hash <node>` — preview against the live host.

Step 2 is non-optional. A bundle that "passes `bw test`" with no consumer
is proven only to parse.
```

### Commit 4 — nodes carry only node-specific metadata (Gap 3)

**`bundles/AGENTS.md` Conventions** — new bullet:

```markdown
- **Bundles own application-wide knowledge; nodes carry only the few
  per-host knobs the bundle actually needs.** When designing a bundle,
  identify the per-node knobs (e.g. domain, uplink interface, a
  vault-id suffix) and put everything else in `defaults`, or in a
  reactor that derives from those knobs. Per-node random secrets
  belong in `defaults` via `repo.vault.random_bytes_as_base64_for(...)`
  keyed on the node — not in the node file. See
  `bundles/left4me/metadata.py:10` (`secret_key` derived in defaults)
  and `bundles/postgresql/metadata.py:4` (vault-derived `password_for`
  at module scope).
```

**`nodes/AGENTS.md` Pitfalls** — new bullet:

```markdown
- **Bloated per-node metadata is usually a bundle smell.** If a
  bundle's metadata block in the node file has more than 3-5 keys,
  the bundle is probably under-using `defaults` / reactors. Push the
  contribution into the bundle (see
  [`bundles/AGENTS.md`](../bundles/AGENTS.md#conventions)) rather than
  growing the node file.
```

### Commit 5 — reactors must read metadata or be defaults (Gap 4)

**`bundles/AGENTS.md` Pitfalls** — new bullet:

```markdown
- **Reactors must read metadata.** If a reactor body returns a static
  dict without calling `metadata.get(...)`, bw raises
  `ValueError: <reactor> on <node> did not request any metadata, you
  might want to use defaults instead` once a node consumes the bundle.
  Fix: fold the contribution into `defaults`. The rule applies even
  when the reactor writes into another bundle's namespace — a static
  contribution to e.g. `nftables/output` belongs in `defaults`, where
  bw merges it with other bundles' contributions.
```

### Commit 6 — `triggers` invariant + self-healing + `unless` (Gaps 5+6)

**`bundles/AGENTS.md` Pitfalls** — two new bullets (Gap 6's `unless`
semantics fold into the second; cleaner than three bullets):

```markdown
- **`triggers` ↔ `triggered: True` invariant.** Any item listed in
  another's `triggers` list must declare `triggered: True`. bw
  enforces this at `bw test` time: *"…triggered by …, but missing
  'triggered' attribute"*. Corollary: an action can't be both in an
  upstream `triggers` list AND self-healing every apply — pick one.

- **Triggered actions don't recover from partial failure.** When an
  upstream item's apply succeeds but its triggered downstream action
  fails, subsequent applies can't recover via the trigger chain —
  upstream is "already in desired state" and never re-triggers. For
  actions that must self-heal (pip installs, chowns, migrations),
  drop `triggered: True` and gate the command with `unless:
  <fast-check>`. `unless` is a shell command on the target host whose
  exit status decides whether the main command runs (exit 0 = skip);
  it's checked at fire time, after `triggered:` filtering.
```

## Out of scope

- Gaps 7–12 — deferred. The maintainer re-engages after this round.
- Bundle behaviour changes. Pure docs.
- `bw apply` / `bw run` — not authorised this session.

## Constraints

- Don't echo decrypted secrets in commit messages or new doc text.
- Don't restore `*.py_` parked nodes.
- After each commit, `.venv/bin/bw test` must pass.
- No push.
