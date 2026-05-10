# nodes/

## What's here

One file per node, ~22 in total. Each file is a single Python
expression (a dict literal) describing one machine: hostname, groups,
bundles, and metadata.

## Loader mechanism

`nodes.py` (top of the repo) walks `nodes/`, reads each `*.py` file,
runs `eval()` on its content, and then *demagifies* the result —
resolving any `!password_for:`, `!decrypt:`, `!decrypt_file:`, and
`!32_random_bytes_as_base64_for:` magic strings via `repo.vault`. See
[`docs/agents/conventions.md#secrets`](../docs/agents/conventions.md#secrets)
for the magic-string list.

This loader shape has consequences:

- **No top-level imports.** The file must be a single expression. No
  `import os`, no `def`, no `if`. Use `repo.libs.<x>` from bundle code
  if you need a helper.
- **Silent drop on parse failure.** Vanilla bundlewrap omits a node
  whose file fails to eval. The maintainer's `groups.py` was patched
  in commit `dc40295` to print the error; the node-loader prints
  on `nodes.py` errors via the same shape. Symptom either way:
  `bw nodes` lists fewer nodes than expected.

## Conventions

- **Filename = node name.** `home.server.py` defines the node `home.server`.
- **Naming pattern: `<location>.<role>.py`.** Examples:
  `home.server.py`, `htz.mails.py`, `ovh.left4me.py`,
  `mseibert.freescout.py`.
- **`*.py_` parks a node** without loading it. Used to keep
  decommissioned-but-not-deleted configs in tree (e.g.
  `htz.l4d2.py_`). The loader only matches `*.py`.
- **Magic strings only resolve here.** `!password_for:` etc. work in
  node files; in groups, bundles, or items they don't — call
  `repo.vault.<verb>(...)` directly there.

## How to add a new node

1. Create `nodes/<location>.<role>.py` with a single dict expression:

   ```python
   {
       'id': 'a-uuid-or-stable-name',
       'hostname': '<dns-name-or-ip>',
       'groups': {
           'debian-13',
           'monitored',
           # …
       },
       'bundles': {
           # only bundles not provided by the groups above
       },
       'metadata': {
           # node-local overrides and required keys
       },
   }
   ```

2. Add to relevant `groups/<axis>/<x>.py` if group membership is the
   attachment point (preferred over per-node `bundles` lists).

3. Verify:
   - `bw nodes` — your node should appear.
   - `bw nodes <node> -a groups` — confirm group membership resolved
     as expected (`bw groups -n <node>` does **not** exist).
   - `bw metadata <node>` — confirm merged metadata.

## Pitfalls

- **Renaming a node renames the node.** Vault entries (anything keyed
  on `!password_for:<node>`), `bw hash` records, and ssh known_hosts
  associations all key on node name. Search-and-replace before
  renaming, or vault lookups silently return new (wrong) values.
- **Don't restore `_old` or `*.py_` files** without checking
  [`conventions.md#suspension-and-soft-delete-idioms`](../docs/agents/conventions.md#suspension-and-soft-delete-idioms).
  These are intentional parks/buffers, not bugs.
- **`id` must be unique.** A pre-apply hook (`hooks/unique_node_ids.py`)
  enforces this; duplicate IDs fail `bw test` and `bw apply`.
- **Bloated per-node metadata is usually a bundle smell.** If a
  bundle's metadata block in the node file has more than 3-5 keys,
  the bundle is probably under-using `defaults` / reactors. Push the
  contribution into the bundle (see
  [`bundles/AGENTS.md`](../bundles/AGENTS.md#conventions)) rather than
  growing the node file.

## See also

- [`groups/AGENTS.md`](../groups/AGENTS.md) — group-membership patterns,
  how metadata merges along the chain.
- [`docs/agents/conventions.md`](../docs/agents/conventions.md) —
  demagify magic-strings, naming, eval-loader constraints.
- Fork's [`AGENTS.md`](https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md)
  — node attribute reference (`hostname`, `username`, `dummy`, etc.).
