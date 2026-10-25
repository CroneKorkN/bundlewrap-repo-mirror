# libs/

## What's here

Shared Python helpers reachable from any bundle as
`repo.libs.<modulename>.<symbol>`. One module per file (no packages).
Discovery is by `ls libs/` plus the one-line module docstring at the
top of each file.

```sh
head -1 libs/*.py
```

## Conventions

- **One file per module.** Filename (without `.py`) is the
  importable name. `libs/wireguard.py` exposes `repo.libs.wireguard`.
- **One-line module docstring.** Every `libs/*.py` starts with
  `"""<name>: <one-line purpose>."""` so `ls + head` is a working index.
  Add one when introducing a new lib; the rule is enforced by the
  Phase-0 baseline (`grep -L '"""' libs/*.py` should report zero
  files).
- **Pure helpers, no I/O at import.** Libs are imported on every `bw`
  invocation. Heavy work or filesystem reads at module scope slow the
  whole repo. Use functions, not module-level side effects.
- **No magic-string demagification here.** Libs receive already-
  resolved values from bundles or nodes. Don't pass `!password_for:`
  strings into libs — they won't be resolved.
- **`repo` and `vault` are globals available at runtime.** A few libs
  (`wireguard.py`, etc.) reach `repo.vault.<verb>(...)` directly.
  That's intentional inside libs, since libs run in the same loader
  scope as bundles.

## How to add a helper

1. Either extract from a bundle that's growing complex, or add a new
   `libs/<name>.py` file.
2. Top line: `"""<name>: <one-line purpose>."""`.
3. Pure functions only; document side effects in the docstring if any
   slip through.
4. Use it from `bundles/<x>/items.py` or `metadata.py` as
   `repo.libs.<name>.<symbol>(...)`.

## Pitfalls

- **Lib changes have repo-wide blast radius.** Every bundle that
  imports the lib re-evaluates on the next `bw test` / `bw apply`.
  Before changing a lib's API, find consumers:

  ```sh
  git grep -l 'repo.libs.<x>'
  ```

- **`@cache` is your friend** for deterministic key derivations
  (`wireguard`, `rsa`, `ssh`); without it, `bw` recomputes per call,
  which is slow.
- **Hashable wrappers.** `libs/hashable.py` exists because raw dicts
  and sets aren't hashable, so you can't put them inside metadata
  sets. Wrap with `repo.libs.hashable.hashable(...)` before nesting.

## See also

- [`bundles/AGENTS.md`](../bundles/AGENTS.md) — when to extract a
  helper into `libs/` instead of duplicating across bundles.
- [`docs/agents/conventions.md`](../docs/agents/conventions.md) —
  vault, demagify, naming.
- The fork's [`AGENTS.md`](https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md)
  — `repo.libs` mechanism.
