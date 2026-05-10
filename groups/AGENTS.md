# groups/

## What's here

Groups attach bundles and shared metadata to nodes. One file per group,
organized by axis:

```
groups/
├── all.py                     # universal base (every node belongs)
├── applications/<x>.py        # role-shaped groups (mailserver, monitored, …)
├── locations/<x>.py           # physical/network location (home, htz, …)
├── machine/<x>.py             # hardware kind (hardware, hetzner-cloud, raspberry-pi)
└── os/<x>.py                  # OS major/variant (debian-13, debian-13-pve, routeros, …)
```

## Loader mechanism

`groups.py` (top of the repo) walks `groups/` and runs `eval()` on each
`*.py`. Same eval-as-expression rule as
[`nodes/`](../nodes/AGENTS.md#loader-mechanism): one dict literal, no
top-level imports, no statements. Errors print and the group is skipped
— a real foot-gun, since a missing group silently changes node
membership.

**Group files are *not* demagified.** Magic strings like
`!password_for:<x>` only resolve in `nodes/*.py`. Inside a group file,
call `repo.vault.<verb>(...)` directly.

## Inheritance and merge order

Metadata merges along this chain:

```
all → location → os → machine → applications → node
```

Per-axis subdirs are conventional, not enforced — `bw` doesn't read the
subdir. Each group lists its `supergroups`, and `bw` resolves the DAG.
Membership is set-union; metadata merge follows the order above, with
the node's own `metadata` block winning last.

## Conventions

- **One group per file.** Filename without `.py` = group name. Subdir
  groups them by axis for humans, not for bw.
- **Family files for OS variants.** Common parent + per-variant child.
  Example: `debian-13-common.py` is shared by `debian-13.py` and
  `debian-13-pve.py`. Use this pattern when introducing
  related-but-distinct OS group families.
- **`all.py` is the universal default.** Currently empty (`{}`); kept
  for the rare repo-wide opt-in.

## How to add a group

1. Pick the right axis subdir (or root `all.py` for universal default).
2. Create `groups/<axis>/<name>.py` as a single dict expression:

   ```python
   {
       'supergroups': [
           # parent groups whose bundles/metadata this one extends
       ],
       'bundles': [
           # bundles every member of this group should have
       ],
       'metadata': {
           # shared metadata for members
       },
   }
   ```

3. Wire the group into the relevant `nodes/*.py` (`'groups': {...}`)
   or `groups/*.py` `supergroups` list.

4. Verify with `bw nodes <node> -a groups` and `bw metadata <node>`.

## How to add a new OS major (recipe)

Pattern from prior debian-12 → debian-13 work:

1. Add `groups/os/debian-N.py` and `groups/os/debian-N-common.py`
   parallel to the existing files. Don't edit in place.
2. Add `data/apt/keys/debian-N-*.{asc,gpg}` for the new release's
   signing keys. See
   [`commands.md#apt-key-changes-need-offline-verification`](../docs/agents/commands.md#apt-key-changes-need-offline-verification)
   before pushing keys live.
3. Bump dependent bundles that branch on `os_version` /
   `os_codename` (`bundles/bind/items.py`, etc.).
4. Bump affected nodes' `groups` lists one at a time. Apply, watch.
5. Delete the old OS group file once no node references it.

## Pitfalls

- **`bw groups -n <node>` doesn't exist.** Use
  `bw nodes <node> -a groups`.
- **Cycles.** A group can't be its own supergroup transitively;
  `bw test` catches this but the error message is terse.
- **Silent eval failure.** A group file with a syntax error is skipped
  and prints a one-line error. If a node loses bundles unexpectedly,
  scan `groups.py` output for the error.

## See also

- [`nodes/AGENTS.md`](../nodes/AGENTS.md) — node files; how
  `groups: {...}` attaches groups.
- [`docs/agents/conventions.md`](../docs/agents/conventions.md) —
  inheritance order, naming conventions, eval-loader constraints.
- Fork's [`AGENTS.md`](https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md)
  — group attribute reference, metadata-merge semantics.
