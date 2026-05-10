# data/

## What's here

Out-of-bundle data assets consumed by one or more bundles. Each subdir
maps to a consumer:

```
data/
├── apt/keys/                   # binary GPG keys for apt sources
├── grafana/rows/               # Mako-templated dashboard panels (Python)
├── nginx/                      # nginx snippets shared across vhosts
├── homeassistant/, mailman/, nextcloud/, ...
└── network.py                  # repo-wide network metadata (one-off file)
```

## Two distinct content models

Same directory shape, different content kinds. When you add a new
`data/<x>/` subdir, declare which model it follows:

| Model | Example | Consumer |
|---|---|---|
| **Binary / static**          | `data/apt/keys/*.{asc,gpg}` | `bundles/apt` reads files at apply time |
| **Python module / template** | `data/grafana/rows/*.py`, `data/routeros-monitoring/*.py` | bundle `import`s and renders |

If a data asset is read by **exactly one bundle**, prefer
`bundles/<x>/files/` instead of `data/<x>/`. `data/` is for
shared / multi-consumer artifacts. Single-instance evidence: commit
`78a8abc` moved `mikrotik.mib` *out* of `data/` *into* the bundle for
this reason.

## Conventions

- **One subdir per consumer.** Subdir name = consumer bundle name
  (`data/apt/`, `data/nextcloud/`).
- **`network.py` exception.** A single file at `data/network.py` holds
  repo-wide network metadata; it doesn't belong to one bundle. Treat
  it as cross-cutting infrastructure metadata.

## How to add data

1. Decide the content model (binary or Python).
2. `mkdir data/<consumer>/`.
3. Drop assets in.
4. The consumer bundle (`bundles/<consumer>/items.py` or
   `metadata.py`) reads them via `repo.path` + `os.path.join` or
   similar.

## Pitfalls

- **Apt keys** trigger an offline-verify rule before they're committed.
  See [`commands.md#apt-key-changes-need-offline-verification`](../docs/agents/commands.md#apt-key-changes-need-offline-verification).
- **Mako-templated Python data** evaluates at bundle render time. Side
  effects in those modules slow the whole repo (same caveat as
  [`libs/`](../libs/AGENTS.md)).

## See also

- [`bundles/AGENTS.md`](../bundles/AGENTS.md) — when bundle `files/`
  beats `data/`.
- [`docs/agents/commands.md`](../docs/agents/commands.md) — apt-key
  verification rule.
