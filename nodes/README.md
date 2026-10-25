# nodes/

## What's here

One file per node. Each file is a single Python
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
- **A file that fails to eval aborts `bw`.** Nothing is skipped.

## Conventions

- **Filename = node name.** `home.server.py` defines the node `home.server`.
- **Naming pattern: `<location>.<role>.py`.** Examples:
  `home.server.py`, `ovh.mails.py`, `mseibert.freescout.py`; a lone
  device without a location keeps its plain name (`macbook.py`).
- **Only `*.py` loads.** Any other suffix keeps a file out of `bw`.
- **Magic strings only resolve here.** `!password_for:` etc. work in
  node files; in groups, bundles, or items they don't — call
  `repo.vault.<verb>(...)` directly there.

## How to add a new node

1. Create `nodes/<location>.<role>.py` with a single dict expression:

   ```python
   {
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
           'id': '<a new uuid>',
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
- **`metadata/id` must be unique.** A pre-apply hook (`hooks/unique_node_ids.py`)
  enforces this; duplicate IDs fail `bw test` and `bw apply`.
- **Bloated per-node metadata is usually a bundle smell.** If a
  bundle's metadata block in the node file has more than 3-5 keys,
  the bundle is probably under-using `defaults` / reactors. Push the
  contribution into the bundle (see
  [`bundles/README.md`](../bundles/README.md#conventions)) rather than
  growing the node file.

## See also

- [`groups/README.md`](../groups/README.md) — group-membership patterns,
  how group and node metadata merge.
- [`docs/agents/conventions.md`](../docs/agents/conventions.md) —
  demagify magic-strings, naming, eval-loader constraints.
- Fork's [`AGENTS.md`](https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md)
  — node attribute reference (`hostname`, `username`, `dummy`, etc.).
