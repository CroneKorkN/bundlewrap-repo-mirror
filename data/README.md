# data/

## What's here

Out-of-bundle data assets consumed by one or more bundles. Each subdir
maps to a consumer:

```
data/
├── apt/keys/                   # binary GPG keys for apt sources
├── grafana/rows/               # dashboard rows as python dict literals
├── nginx/                      # nginx snippets shared across vhosts
└── nextcloud/, yourls/, ...    # vhost templates, see nginx/vhosts content
```

## Two distinct content models

Same directory shape, different content kinds. When you add a new
`data/<x>/` subdir, declare which model it follows:

| Model | Example | Consumer |
|---|---|---|
| **Binary / static**          | `data/apt/keys/*.{asc,gpg}` | `bundles/apt` reads files at apply time |
| **Python literal / template** | `data/grafana/rows/*.py`, `data/*/vhost.conf` | grafana reads the rows with `eval()`, nginx renders the vhosts with mako |

If a data asset is read by **exactly one bundle**, prefer
`bundles/<x>/files/` instead of `data/<x>/`. `data/` is for
shared / multi-consumer artifacts. Single-instance evidence: commit
`78a8abc` moved `mikrotik.mib` *out* of `data/` *into* the bundle for
this reason.

## Conventions

- **One subdir per consumer or per subject.** `data/apt/` belongs to
  the apt bundle; `data/<app>/vhost.conf` is a vhost template the nginx
  bundle renders for the node that sets `nginx/vhosts/<host>/content`.

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
- **Python data is `eval()`ed** at item build time. Keep it plain
  literals, no side effects (same caveat as
  [`libs/`](../libs/README.md)).

## See also

- [`bundles/README.md`](../bundles/README.md) — when bundle `files/`
  beats `data/`.
- [`docs/agents/commands.md`](../docs/agents/commands.md) — apt-key
  verification rule.
