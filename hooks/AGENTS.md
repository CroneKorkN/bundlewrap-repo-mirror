# hooks/

## What's here

Repo-level lifecycle hooks. Each `*.py` exports one or more functions
named after the lifecycle event they listen to (`apply_start`,
`node_apply_start`, `node_run_start`, `test`, `test_node`, …). Bw
discovers them by importing each module from `hooks/`.

Discovery is by `ls hooks/` + the one-line docstring at the top of
each file:

```sh
head -1 hooks/*.py
```

## Conventions

- **One-line module docstring.** Every `hooks/*.py` starts with
  `"""<name>: <one-line purpose>."""`. Add one when introducing a new
  hook; baseline is enforced by `grep -L '"""' hooks/*.py`.
- **Function name = event name.** Bw calls
  `apply_start(repo, target, nodes, interactive=False, **kwargs)`,
  `node_apply_start(repo, node, interactive, **kwargs)`,
  `test(repo, **kwargs)`, etc. Always accept `**kwargs` so future bw
  arguments don't break the hook.
- **Test gates use `test` / `test_node`.** Anything that should fail
  `bw test` (and therefore CI / pre-apply sanity) goes here; avoid
  doing test-style assertions in `apply_start`.

## How to add a hook

1. Pick the lifecycle event (see fork's `AGENTS.md` for the full list).
2. Create `hooks/<name>.py` with the matching function and a
   docstring.
3. Run `bw test` once to confirm the hook loads cleanly.

## Pitfalls

- **A hook that errors at import breaks every `bw` invocation** that
  fires the hook's lifecycle — including `bw test` itself, which
  defeats the obvious diagnostic. Test new hooks in isolation first:

  ```sh
  bw debug -c "import sys; sys.path.insert(0, 'hooks'); import <hookmodule>"
  ```

  Iterate there until the import is clean, then commit.
- **Hooks have access to the full repo (`repo`, `node`, `nodes`).**
  Don't make them block on network unless that's the explicit purpose
  (e.g. `test_ptr_records.py` does `dig` against `9.9.9.9`).
- **Order is not guaranteed across hook files.** Two hooks that both
  define `apply_start` will both fire; don't assume which runs first.

## See also

- [`docs/agents/conventions.md`](../docs/agents/conventions.md) —
  files-not-to-touch, vault rules.
- [`docs/agents/commands.md`](../docs/agents/commands.md) — test
  workflow.
- Fork's [`AGENTS.md`](https://github.com/CroneKorkN/bundlewrap/blob/main/AGENTS.md)
  — full hook lifecycle and signatures.
