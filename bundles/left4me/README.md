# left4me

L4D2 game-server management platform: a Flask web UI on gunicorn that
provisions per-instance srcds servers via templated systemd units, with
kernel-overlayfs layering for shared installations + per-overlay maps,
and uid-based DSCP/priority marking on the egress path so CAKE on the
external interface prioritizes srcds UDP over bulk traffic.

## Metadata

```python
'metadata': {
    'left4me': {
        'domain': 'whatever.tld',  # required — the only per-node knob
        # Everything below is optional and has a sensible default in the
        # bundle. Override per-node only if the default is wrong:
        # 'git_url': 'git@git.sublimity.de:cronekorkn/left4me',
        # 'git_branch': 'master',
        # 'gunicorn_workers': 1,
        # 'gunicorn_threads': 32,
        # 'job_worker_threads': 4,
        # 'port_range_start': 27015,
        # 'port_range_end': 27115,
        # secret_key is auto-derived per node
        # (repo.vault.random_bytes_as_base64_for f'{node.name} left4me secret_key').
    },
},
```

The bundle's `derived_from_domain` reactor reads `left4me/domain` and
emits the corresponding `nginx/vhosts`, `letsencrypt/domains`,
`monitoring/services/left4me-web` (HTTPS health check), and the game-
port `nftables/input` accept rules. Backup paths
(`/var/lib/left4me`, `/etc/left4me`) are set-merged into `backup/paths`
from defaults. None of these need to be declared per-node.

## What this bundle does

The bundle delivers to `ovh.left4me` a mix of:

### Target-side symlinks into the left4me checkout

After `git_deploy:/opt/left4me/src` (root-owned — left4me cannot rewrite
its own deployment artifacts at runtime), ckn-bw creates symlinks from
canonical on-host paths into the checkout:

| On-host path | Source in checkout |
|---|---|
| `/etc/sudoers.d/left4me` | `deploy/files/etc/sudoers.d/left4me` |
| `/etc/sysctl.d/99-left4me.conf` | `deploy/files/etc/sysctl.d/99-left4me.conf` |
| `/etc/systemd/system/left4me-web.service.d/10-hardening.conf` | `deploy/files/etc/systemd/system/left4me-web.service.d/10-hardening.conf` |
| `/etc/systemd/system/left4me-server@.service.d/10-hardening.conf` | `deploy/files/etc/systemd/system/left4me-server@.service.d/10-hardening.conf` |
| `/usr/local/libexec/left4me/{left4me-overlay,left4me-systemctl,left4me-journalctl,left4me-script-sandbox}` | `deploy/scripts/libexec/*` |
| `/usr/local/sbin/left4me` | `deploy/scripts/sbin/left4me` |

The hardening drop-ins and sudoers are the application's own security
knowledge — they live in the left4me repo and are version-controlled there.
The privileged helpers are also application code. The symlink pattern
lets bw manage placement without duplicating content.

Design rationale:
`left4me/docs/superpowers/specs/2026-05-15-deployment-responsibility-design.md`.

### Reactor-emitted units (per-host shape)

Via `systemd/units` metadata in `metadata.py` (consumed by `bundles/systemd/`):

- `left4me-web.service` — gunicorn on `127.0.0.1:8000`; worker/thread
  counts from `web.env.mako`. TLS terminates upstream.
- `left4me-server@.service` — per-instance srcds template; `SocketBindAllow=`
  ranges from metadata.
- `l4d2-game.slice` / `l4d2-build.slice` — cgroup slices with per-host
  `AllowedCPUs=` from `left4me/system_cpus`.
- `system.slice.d/99-left4me-cpuset.conf` + `user.slice.d/99-left4me-cpuset.conf`
  — host CPU-set drop-ins, same source.

### bw `files{}` — templated env files

- `host.env.mako` → `/etc/left4me/host.env`
- `web.env.mako` → `/etc/left4me/web.env`
- `sandbox-resolv.conf` → `/etc/left4me/sandbox-resolv.conf`

### Action chains — deploy lifecycle

- `git_deploy` → `uv_sync` (`uv sync --frozen` against the workspace's
  committed `uv.lock`; hatchling PEP 660 editable, doesn't touch source)
  → `alembic_upgrade` → `seed_overlays` + web restart.
- One-shot bootstrap: `install_uv` downloads a pinned `uv` binary
  (SHA256-verified) into `/usr/local/bin` because `uv` isn't in Trixie's
  apt archive. `unless`-gated, so it's a no-op once the version pin is
  installed; re-runs only when the constant is bumped.
- Idempotent gates: `chmod-sudoers` (0440 root:root), `chmod-scripts` (0755 root:root).
- Post-git-deploy reloads: `systemctl daemon-reload`, `sysctl --system`.
- Post-apply self-test: `verify-hardening-dropins` (asserts the drop-ins are
  loaded by the live units before declaring apply done).

### System user

`left4me` (uid/gid 980, home `/var/lib/left4me`, mode 0755) — the same uid
hosts the web app, gameservers, and the script-overlay sandbox unit (which
drops privileges via systemd-run with a fully hardened transient service).
Runtime mutable state lives under `/var/lib/left4me/`; `/opt/left4me/`
stays as a root-owned deploy-artifact root.

### nftables / nginx / monitoring

- Contributes uid-based DSCP/priority marks for srcds UDP egress to
  `nftables/output` (via `defaults`).
- `derived_from_domain` reactor emits the corresponding `nginx/vhosts`,
  `letsencrypt/domains`, and `monitoring/services/left4me-web` (HTTPS
  health check).

## Gotchas

- **Requires `bundles/nftables` and `bundles/systemd` on the node.** The
  bundle asserts membership at `bw test` time. On Debian-13 these ride
  in via the `debian-13` group, so attaching the bundle to a Debian-13
  node is enough.
- **`left4me-web.service` does not have `NoNewPrivileges=true`.** This is
  intentional — workers `sudo` the privileged helpers; `NoNewPrivileges`
  would block setuid escalation. Per-instance `server@.service` units
  *do* have it.
- **CAKE shaping is configured separately**, via
  `network/<iface>/cake` on the node (consumed by `bundles/network/`),
  not by this bundle.
- **First-run admin user is manual.** After `bw apply`, ssh to the host and
  bootstrap the admin via the `left4me` wrapper (it sources the env files,
  drops to the `left4me` user, and runs the flask CLI):
  `sudo left4me create-user <username> --admin` (prompts for password via
  the flask CLI, or set `LEFT4ME_ADMIN_PASSWORD` first). The bundle
  deliberately doesn't seed an admin to keep credentials out of the
  metadata pipeline. The same `left4me` wrapper accepts any other flask
  subcommand: `sudo left4me seed-script-overlays <dir>`,
  `sudo left4me routes`, `sudo left4me shell`, etc.
- **CPU isolation is managed by this bundle**, driven by one required
  per-node knob: `left4me/system_cpus` — a set of int CPU ids that
  pins `system.slice` / `user.slice` / `l4d2-build.slice`. The
  complement (`set(range(vm/threads)) - system_cpus`) pins
  `l4d2-game.slice`. On HT hosts, list both SMT siblings of every
  physical core you want to reserve for system, otherwise games end
  up sharing L1/L2 with system. Find pairings via
  `/sys/devices/system/cpu/cpu<n>/topology/thread_siblings_list`. On
  the prod node (`ovh.left4me`, 4 physical / 8 threads, pairings
  (0,4) (1,5) (2,6) (3,7)) the node sets `'system_cpus': {0, 4}` to
  reserve physical core 0 entirely. `l4d2-game.slice` and
  `l4d2-build.slice` carry `AllowedCPUs=` inline on their unit
  definitions; `system.slice` and `user.slice` get drop-ins registered
  under `systemd/units` with the `'<parent>.d/<basename>.conf'` key
  convention (same shape nginx and autologin use), landing at
  `/usr/local/lib/systemd/system/<slice>.d/99-left4me-cpuset.conf`.
  The reactor raises if `system_cpus` includes CPUs outside
  `[0, vm/threads)` or leaves no cores for games.
- **Kernel feature requirement:** kernel-overlayfs (`CONFIG_OVERLAY_FS`).
  Standard on debian-13.
- **Game ports** open by the web app on demand in the range 27015-27115
  (UDP+TCP). Add corresponding accept rules to `nftables/input` per
  node if the host's policy is default-drop on input.
- **Pinned UIDs/GIDs (980/981).** Chosen for deterministic ownership
  across rebuilds and backup restores. If you add another bundle that
  pins UIDs in this repo, make sure it doesn't collide.

## Slice support requires `bundles/systemd` ≥ commit cc1c6a5

This bundle's `l4d2-game.slice` and `l4d2-build.slice` units rely on
`bundles/systemd/items.py` accepting the `.slice` extension. Older
revisions raised `Exception(f'unknown type slice')` at apply time.
The repo-wide `bw test` will catch this if it regresses.
