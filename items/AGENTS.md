# items/

## What's here

Custom item types — each `*.py` is a `bundlewrap.items.Item` subclass
that adds a new item kind to the repo (e.g. `download:` from
`items/download.py`).

Currently:

- `items/download.py` — verifying file downloads with sha256 / GPG.
  (Originally from `bundlewrap/plugins/item_download`; vendored in
  because bw 4 dropped plugin support and it never came back.)

## Conventions

- **Filename = item-type slug.** `items/download.py` defines item
  type `download:`. The class's `BUNDLE_ATTRIBUTE_NAME` is the dict
  name in `items.py` (`downloads = {...}`).
- **Subclass `bundlewrap.items.Item`.** See the upstream
  [bundlewrap docs on writing item types](https://docs.bundlewrap.org/dev/items/)
  for the contract: `ITEM_ATTRIBUTES`, `fix`, `sdict`, `cdict`,
  `display_dicts`, etc.
- **No metadata-reactor integration unless deliberate.** Item types
  get to declare `NEEDS_STATIC` (cross-type ordering hints) — use it
  sparingly; broad `NEEDS_STATIC` slows the whole DAG.

## When to write a new custom item type vs. use `file:` (or
`action:`, etc.)

| Situation | Use |
|---|---|
| One-off shell command at apply time              | `action:` in the bundle |
| File whose source is in `bundles/<x>/files/`     | `file:` |
| File you have to **fetch + verify** at apply     | `download:` (already custom) |
| Behavior bw doesn't model and that recurs across bundles | new custom item |

If you only need it once, an `action:` is almost always enough.
Custom item types are repo-wide and load on every `bw` invocation —
the cost is paid forever.

## How to add a custom item type

1. Pick a slug (lowercase, no underscore).
2. Create `items/<slug>.py` with an `Item` subclass.
3. `bw test` — broken item types break the loader for every bundle
   that uses them, so test in isolation first.
4. Document the contract in the file's module docstring.

## Pitfalls

- **Items affect the whole repo.** A change to `items/<x>.py` runs in
  every node's apply. Treat custom items the way you treat `libs/` —
  pure, fast, side-effect-free at import.
- **`NEEDS_STATIC` is a coarse hammer.** It enforces ordering across
  *all* nodes for *all* items of those types; don't add unless
  you've actually hit ordering issues.

## See also

- [`bundles/AGENTS.md`](../bundles/AGENTS.md) — items are consumed by
  `items.py` in each bundle.
- Fork's [`AGENTS.md`](https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md)
  — built-in item-type catalogue.
