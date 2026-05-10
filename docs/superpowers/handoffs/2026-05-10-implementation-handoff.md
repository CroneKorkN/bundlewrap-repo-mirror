# Handoff — agent-friendly docs for ckn-bw (status: complete)

The 2026-05-10 work is finished. This file replaces the original
multi-page handoff (which described work that's now done plus a
Phase 2 that was dropped). Kept as a breadcrumb so future agents
know what landed.

## What landed

- **Phase 0** (`730625e`) — top-of-file docstrings on every
  `libs/*.py` and `hooks/*.py`; `# purpose:` headers on every
  `bin/*` script. Discovery is `ls + head -1`.
- **Phase 1** (`04558a9`) — root `AGENTS.md` (with `CLAUDE.md`
  symlink), `docs/agents/{conventions,commands}.md`, per-area
  `AGENTS.md` for `bundles/`, `nodes/`, `groups/`, `libs/`,
  `hooks/`, `data/`, `items/`, `bin/`. Mechanism-focused; no
  enumeration of contents.
- **Convention pivot** (`9e1bb2a`) — per-bundle docs are plain
  `README.md`, not `AGENTS.md`. No template. `bundles/AGENTS.md`
  "Per-bundle README" gives loose orientation pointing at the
  more substantial existing READMEs.

`bw test` exit 0 throughout. All internal links in the new docs
resolve. Commits sit on local `master`, none pushed.

## Where current truth lives

- Root entry: [`AGENTS.md`](../../../AGENTS.md) (symlinked to
  `CLAUDE.md`).
- Repo conventions + bw command deltas:
  [`docs/agents/`](../../agents/).
- Per-area docs: `<dir>/AGENTS.md` for each top-level dir.
- Per-bundle docs: existing `README.md` files (~33 of them);
  guidance in [`bundles/AGENTS.md`](../../../bundles/AGENTS.md).
- Self-describing files: `libs/*.py`, `hooks/*.py`, `bin/*`.

## Source documents

- Spec: [`../specs/2026-05-10-agent-friendliness-design.md`](../specs/2026-05-10-agent-friendliness-design.md)
  — read its `§0. Revisions` first; §3 and §7 are now pre-pivot
  intent only.
- User-stories validation: [`../specs/2026-05-10-user-stories-from-history.md`](../specs/2026-05-10-user-stories-from-history.md).
- Implementation plan: `~/.claude/plans/btw-are-you-sure-crystalline-balloon.md`
  (frozen pre-pivot artifact, outside the repo).

## What's open

Nothing planned. Per-bundle README updates are reactive — when a
bundle gets materially edited, top up its `README.md` then. The
~33 existing READMEs vary in quality and shape; that's accepted.

Two minor items the maintainer may want to clean up at some point:

- The implementation plan and the spec's §3 / §7 still describe
  the pre-pivot per-bundle `AGENTS.md` convention. Spec's §0 flags
  this; the plan is a frozen artifact and probably stays as-is.
- The original handoff's verification list mentioned `bw bundles`,
  which isn't a real bw subcommand. Not user-facing in any current
  doc.
