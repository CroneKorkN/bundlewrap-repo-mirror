# bundles/

## Before you start

Read [`docs/agents/conventions.md`](../docs/agents/conventions.md) first
— it covers vault calls, demagify, the `repo.libs.<x>` helpers, and the
files agents must not modify. Skipping it leads to subtly broken bundles
(vault calls in the wrong place, dict-in-set `TypeError` because of
unhashable nesting, etc.).

For bundlewrap-language reference (item types, dep keywords,
`metadata_reactor`, `defaults`, item-file template syntax) see the fork's
[`AGENTS.md`](https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md)
and its [`docs/content/guide/item_file_templates.md`](https://github.com/CroneKorkN/bundlewrap/blob/main/docs/content/guide/item_file_templates.md).

## What's here

103 bundles. Each is a directory `bundles/<name>/` containing some of:

```
bundles/<name>/
├── items.py        # the items this bundle creates (files, services, packages, …)
├── metadata.py     # `defaults` + `@metadata_reactor` functions
├── files/          # static or templated file payloads referenced from items.py
├── AGENTS.md       # this bundle's doc (template at AGENTS.template.md)
└── README.md       # legacy; being phased out (see "Documentation transition" below)
```

## Conventions

- **Bundle names** are lowercase, hyphen-separated: `backup-server`,
  `bind-acme`, `dm-crypt`. No underscores in new bundle names — see
  [`conventions.md#naming-conventions`](../docs/agents/conventions.md#naming-conventions).
- **`items.py`** is plain Python; it produces `files = {...}`,
  `pkg_apt = {...}`, `svc_systemd = {...}`, etc. dicts at module scope.
  Cross-item dependencies use `needs` / `triggers` / `triggered_by` —
  see the fork's `AGENTS.md` for the full keyword cheat sheet.
- **`metadata.py`** uses `defaults = {...}` for static seed values and
  `@metadata_reactor.provides(...)` for derived values. Reactors are
  pure functions of `(metadata,)` — no side effects, no I/O.
- **Helpers go in [`libs/`](../libs/AGENTS.md)** when they're useful to
  more than one bundle. Don't duplicate logic across bundles.
- **Custom item types** (e.g. `download:`) live in
  [`items/`](../items/AGENTS.md), not per-bundle.

## How to add a new bundle

1. `mkdir bundles/<name>/` (lowercase, hyphenated).
2. Write `items.py` and (if anything is configurable) `metadata.py`.
   Use `repo.libs.hashable.hashable(...)` when you need to nest a dict
   or set inside a metadata set; raw dicts/sets aren't hashable.
3. Drop static payloads into `bundles/<name>/files/`. For Mako-templated
   files, declare `'content_type': 'mako'` on the `file:` item — see
   the fork's
   [item-file-templates guide](https://github.com/CroneKorkN/bundlewrap/blob/main/docs/content/guide/item_file_templates.md).
4. **Wire to nodes.** Either add an entry to the relevant
   [`groups/<axis>/<x>.py`](../groups/AGENTS.md) (preferred for shared
   bundles) or to the node's `bundles` list directly
   ([`nodes/AGENTS.md`](../nodes/AGENTS.md)).
5. Verify, in this order:
   - `bw test` — sanity (loaders + reactors).
   - `bw items <node>` — confirm new items appear on a node that opts in.
   - `bw hash <node>` — confirm the change is what you expected. See
     [`docs/agents/commands.md`](../docs/agents/commands.md) and the
     fork's hash-diff workflow.
6. Create `bundles/<name>/AGENTS.md` from
   [`AGENTS.template.md`](AGENTS.template.md). For a brand-new bundle
   without consumers yet, leave `Depends on` and `Produces` empty or
   marked TBD; fill them in after the first verify run.

## How to remove a bundle

1. `git grep '<name>'` in `nodes/`, `groups/`, and other `bundles/` to
   find references.
2. Remove those references.
3. `rm -rf bundles/<name>/`.
4. `bw test` and `bw nodes` to confirm clean.

## Pitfalls

- **`metadata.py` is evaluated at load time** for *every* node, every
  invocation of `bw`. Heavy work or I/O slows the whole repo. Keep
  reactors pure and fast; pre-compute in `libs/` if you must.
- **Static files vs templates.** `bundles/<x>/files/<f>` is static
  unless the matching `file:` item declares `content_type='mako'`
  (or a templating extension triggers it). To check, read the matching
  `file:` entry in `items.py`.
- **Reactors writing across namespaces.** Some bundles' reactors write
  into other bundles' metadata namespaces (e.g. `nextcloud` writes
  into `apt.packages`, `archive.paths`). When you change such a bundle,
  every consumer's metadata changes too. Per-bundle docs declare these
  in an optional `## Writes into` section — read it before assuming the
  blast radius is local.
- **`bw hash` doesn't accept selectors.** Use `bw hash <node>` per
  literal name; see the fork's runbook.

## Documentation transition

This repo is migrating from bundle `README.md` files to per-bundle
`AGENTS.md` files (one balanced doc per bundle, agents + humans).

- Where both exist, **`AGENTS.md` is canonical**; the `README.md` is
  being phased out.
- ~28 bundle READMEs survive after the seed migration (the seed PR
  folds in 5–10 of them; the rest are addressed lazily on the next
  material edit — Phase 3 leave-as-you-go).
- Phase-3 rule: any time you (or any agent) materially edits a bundle,
  top-up its `AGENTS.md` or create one from
  [`AGENTS.template.md`](AGENTS.template.md). If a stale `README.md`
  is still around in the bundle, fold it in and remove it in the same
  commit.

## See also

- [`AGENTS.template.md`](AGENTS.template.md) — per-bundle doc template.
- [`docs/agents/conventions.md`](../docs/agents/conventions.md) — repo
  idioms (vault, demagify, naming, do-not-touch list).
- [`docs/agents/commands.md`](../docs/agents/commands.md) — repo-specific
  command deltas.
- [`items/AGENTS.md`](../items/AGENTS.md) — custom item types
  (`download:`); when to write a new one vs use `file:`.
- [`libs/AGENTS.md`](../libs/AGENTS.md) — shared helpers.
- Fork's [`AGENTS.md`](https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md)
  — bundlewrap-language reference + safety envelope.
