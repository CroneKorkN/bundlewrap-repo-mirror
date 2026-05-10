# Commands

The canonical bw-command runbook — read-only allowlist, three-tier
safety envelope, after-change table, hash-diff workflow, `bw debug`
sketch — lives in the fork's
[`AGENTS.md`](https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md).
Read that first.

This file collects only the deltas specific to `ckn-bw`.

## Apt-key changes need offline verification

Editing files under `data/apt/keys/*.{asc,gpg}` rotates a signing key
the whole apt subsystem trusts. Trial-and-error with `bw apply` is the
*failure* path: a wrong key blocks unattended upgrades cluster-wide
until corrected manually.

Before touching `data/apt/keys/`:

1. Fetch the new key from its upstream source (project release page,
   `keys.openpgp.org`, etc.).
2. `gpg --show-keys <newkey>` — print the fingerprint.
3. Diff against the fingerprint published by the upstream source.
4. Only after the fingerprint matches, place the file under
   `data/apt/keys/` and let `bundles/apt` consume it on the next
   apply.

## `*.py_` suspended nodes are invisible to `bw nodes`

The repo loader (`nodes.py`) only matches files ending in `.py`. Files
ending in `.py_` are silently skipped. If `bw nodes` reports a node
missing, check whether its file has been parked:

```sh
ls nodes/ | grep '\.py_$'
```

This is the [suspension idiom](conventions.md#suspension-and-soft-delete-idioms),
not a bug.

## Vault output never leaves the terminal

The fork's runbook calls out that `bw debug` resolves vault magic
strings transparently. In `ckn-bw` specifically: never echo, log, or
paste decrypted values, even from a `bw debug -c` one-liner. If you
need to verify a secret resolved correctly, hash or fingerprint it
instead.

See [`conventions.md#secrets`](conventions.md#secrets) for the
demagify magic-string list and the rule's full rationale.
