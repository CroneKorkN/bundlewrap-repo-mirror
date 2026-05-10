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

- Creates system users `left4me` (uid/gid 980, home `/var/lib/left4me`,
  mode 0711) and `l4d2-sandbox` (uid/gid 981, no home, used by bwrap
  script-overlay builds).
- Drops privileged helpers under `/usr/local/libexec/left4me/`
  (`left4me-systemctl`, `left4me-journalctl`, `left4me-overlay`,
  `left4me-script-sandbox`) plus a tight sudoers file (validated with
  `visudo -cf` before install).
- `git_deploy`s the left4me repo to `/opt/left4me/src`, builds a venv at
  `/opt/left4me/.venv`, `pip install -e`s both `l4d2host` and `l4d2web`,
  runs `alembic upgrade head` and `flask seed-script-overlays`, then
  enables `left4me-web.service`.
- Emits four systemd units via `systemd/units` metadata (consumed by
  `bundles/systemd/`):
  - `left4me-web.service` — gunicorn on `127.0.0.1:8000` (TLS terminates upstream).
  - `left4me-server@.service` — per-instance srcds template, started on
    demand by the web app via the `left4me-systemctl` helper.
  - `l4d2-game.slice` / `l4d2-build.slice` — cgroup slices for the
    perf-baseline (CPU/IO weights, memory caps).
- Contributes uid-based DSCP/priority marks for srcds UDP egress to
  `nftables/output` (via `defaults`).

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
- **CPU isolation drop-ins are not managed by this bundle.** The
  upstream shell deploy generated `/etc/systemd/system/system.slice.d/
  99-left4me-cpuset.conf` (and siblings for user/build/game slices)
  dynamically based on `nproc --all`. That logic is incompatible with
  static bundle metadata and is out of scope here. Apply CPU isolation
  manually post-deploy if needed.
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
