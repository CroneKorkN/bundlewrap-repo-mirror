# <bundle-name>

<!--
Per-bundle doc template. Copy to `bundles/<name>/AGENTS.md` and fill in.

For a brand-new bundle without consumers yet, leave `Depends on` and
`Produces` empty or marked TBD; fill them in after the first verify run.

Skip the `## Gotchas` section if there are no real gotchas — empty
"Gotchas: none" sections are noise.

Skip the `## Writes into` section unless this bundle's `defaults` or
reactors write into other bundles' metadata namespaces. Most don't.
-->

<1–3 sentences: what this bundle does and when you'd use it.>

## Usage

<How to apply: which group(s) typically include it, or how a node opts
in. Minimal example of node metadata if any keys are required.>

## Metadata

Keys read from `node.metadata`:

```python
{
    '<bundle>': {
        'key':    'value',     # str, required — short note
        'flag':   True,        # bool, default True
        'list':   [],          # list[str], default [] — short note
        'nested': {
            'subkey': 0,       # int, default 0
        },
    },
}
```

## Produces

<Items created: files, services, packages, users, etc. One line each.
Skip if trivially obvious from items.py.>

## Depends on

<Other bundles required, or "none". Note ordering quirks if any.>

## Writes into

<!-- Optional. Most bundles don't write cross-namespace; skip the
section if this bundle doesn't either. List the foreign metadata
namespaces this bundle's `defaults` or reactors populate (e.g.
`apt.packages`, `archive.paths`). Cross-namespace writes are the
single most surprising blast-radius source in this repo — call them
out explicitly. -->

## Gotchas

<Non-obvious behavior, manual one-time steps, known pitfalls. Omit
the section if there are none.>
