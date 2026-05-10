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
└── README.md       # one doc per bundle, for humans and agents (see "Per-bundle README" below)
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
5. **Verify, in this order:**
   - `bw test` — repo-wide parse + cross-cutting hooks. Loads every
     bundle, but reactors don't fire for nodes that haven't opted into
     the bundle yet — bugs in new reactors stay hidden here.
   - **Attach the bundle to a node** (via the node's `bundles` list, or
     a group it belongs to). Until you do, the next steps don't actually
     exercise the bundle.
   - `bw test <node>` — exercises every reactor and item-graph edge for
     that node. This is where most new-bundle bugs surface.
   - `bw items <node> --blame` — confirm items materialise with the
     right paths, authored by the expected bundle.
   - `bw metadata <node> -k <a/b>` — spot-check derived metadata.
   - `bw hash <node>` — preview vs current host state.

   See [`docs/agents/commands.md#bundle-validation-workflow`](../docs/agents/commands.md#bundle-validation-workflow)
   for the rationale.
6. Add a `bundles/<name>/README.md`. See "Per-bundle README" below
   for what to cover.

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
  every consumer's metadata changes too. The bundle's `README.md`
  often calls these out — but the authoritative source is `metadata.py`
  itself; grep `'<other-bundle>':` in the reactors when in doubt.
- **`bw hash` doesn't accept selectors.** Use `bw hash <node>` per
  literal name; see the fork's runbook.

## Per-bundle README

Each bundle has (or should have) a `README.md`. One doc per bundle,
written for humans and agents both. There's no fixed structure —
match the bundle's actual surface, write what helps a future reader
(or future you) avoid trial-and-error.

The existing READMEs vary in quality and shape. For orientation,
look at the bigger ones, not the two-line ones:

- [`bundles/flask/README.md`](flask/README.md) — title + one-sentence
  purpose, a metadata example as a Python dict, then the contract
  the consuming git repo has to satisfy + a logging pitfall. The
  closest thing to a "balanced doc" in tree.
- [`bundles/dm-crypt/README.md`](dm-crypt/README.md) — same shape,
  shorter: purpose + metadata example + one sentence on effect.
- [`bundles/apt/README.md`](apt/README.md) — relevant upstream URLs
  at the top, then a Python metadata example with rich inline
  comments (type / optionality / where keys come from).
- [`bundles/nextcloud/README.md`](nextcloud/README.md) — operational
  scratchpad: iPhone-import recipe, preview-generator commands,
  reset queries. Captures muscle-memory the maintainer would
  otherwise re-learn each time.

Useful things to include, when relevant:

- A sentence or two on what the bundle does and when you'd attach it.
- A metadata example as a Python dict literal, with `#` comments
  on each key (type, required vs default, units, where it comes
  from). This is the cleanest way to communicate the schema and
  matches how `metadata.py` actually looks.
- Anything non-obvious about wiring it up — required keys without
  defaults, group-membership expectations, manual one-time steps.
- Cross-namespace metadata writes, when this bundle's reactors
  populate another bundle's namespace. Easy to miss, cheap to flag.
- Gotchas, debug recipes, failure modes you've actually hit.

What to skip:

- An exhaustive item list — `items.py` is shorter and more accurate.
- Anything that would just rot — version numbers, "TODO" lists,
  change notes. Use git history.

If a single paragraph is enough to say what's worth saying, write a
single paragraph. Verbosity isn't a goal.

Convention going forward is leave-as-you-go: any time you materially
edit a bundle, top up its README (or write one if it's missing).
Don't burn a session bulk-reformatting the existing ones — uneven
quality is part of what we accept in exchange for not blocking other
work.

## See also

- [`docs/agents/conventions.md`](../docs/agents/conventions.md) — repo
  idioms (vault, demagify, naming, do-not-touch list).
- [`docs/agents/commands.md`](../docs/agents/commands.md) — repo-specific
  command deltas.
- [`items/AGENTS.md`](../items/AGENTS.md) — custom item types
  (`download:`); when to write a new one vs use `file:`.
- [`libs/AGENTS.md`](../libs/AGENTS.md) — shared helpers.
- Fork's [`AGENTS.md`](https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md)
  — bundlewrap-language reference + safety envelope.
