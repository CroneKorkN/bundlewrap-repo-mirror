assert node.has_bundle('nftables')
assert node.has_bundle('systemd')
assert node.has_bundle('systemd-timers')


defaults = {
    'left4me': {
        # Application-wide defaults; node only overrides if it really needs to.
        'git_url': 'https://git.sublimity.de/cronekorkn/left4me.git',
        'git_branch': 'master',
        'secret_key': repo.vault.random_bytes_as_base64_for(f'{node.name} left4me secret_key', length=32).value,
        'gunicorn_workers': 1,
        'gunicorn_threads': 32,
        'job_worker_threads': 4,
        # Steam Web API key for the live-state panel's GetPlayerSummaries
        # lookups (persona names + avatars). Empty default — nodes override
        # in their own metadata with the actual key. If left empty in prod,
        # the live-state panel still works but falls back to RCON in-game
        # names and placeholder avatars.
        'steam_web_api_key': '',
        # Whole 27000-block: covers Steam's defaults (27015 game, 27005
        # client/RCON) plus headroom for ad-hoc ports without further
        # nftables changes. Mirrored into LEFT4ME_PORT_RANGE_{START,END}
        # by web.env.mako and into the nftables input rule by the
        # nftables_input reactor below.
        'port_range_start': 27000,
        'port_range_end': 27999,
    },
    'apt': {
        'packages': {
            'p7zip-full': {},
            'nftables': {},
            'iproute2': {},
            'curl': {},
            'ca-certificates': {},
            'python3': {},
            'python3-venv': {},
            'python3-pip': {},
            'python3-dev': {},
            # steamcmd is a 32-bit ELF; needs i386 multiarch + these libs.
            # `_` → `:` is bundlewrap's pkg_apt convention for multiarch
            # names (see pkg_apt.py:48).
            'libc6_i386': {  # installs libc6:i386
                'needs': ['action:left4me_dpkg_add_i386_arch'],
            },
            'lib32z1': {
                'needs': ['action:left4me_dpkg_add_i386_arch'],
            },
        },
    },
    'nftables': {
        # Match deploy/files/usr/local/lib/left4me/nft/left4me-mark.nft.
        # Mark srcds UDP egress (uid left4me) with DSCP EF + skb priority 6
        # so CAKE classifies it into the priority tin.
        'output': {
            'meta skuid "left4me" meta l4proto udp ip dscp set ef meta priority set 0006:0000',
            'meta skuid "left4me" meta l4proto udp ip6 dscp set ef meta priority set 0006:0000',
        },
    },
    'systemd': {
        'services': {
            'left4me-web.service': {
                'enabled': True,
                'running': True,
                'needs': [
                    'action:left4me_alembic_upgrade',
                    'file:/etc/left4me/host.env',
                    'file:/etc/left4me/web.env',
                ],
            },
            # Note: left4me-server@.service is a TEMPLATE — instances are
            # started on-demand by the web app via the left4me-systemctl
            # helper. Don't enable/start it from here.
            # The slices are installed (file present) but don't need
            # enable/start — they're activated implicitly when a unit
            # uses Slice=.
        },
    },
    'backup': {
        # Application-owned paths. Set-merged with backup group / node-level paths.
        'paths': {
            '/var/lib/left4me',
            '/etc/left4me',
        },
    },
    'systemd-timers': {
        # Daily re-fetch of Steam Workshop metadata + .vpk downloads for any
        # item whose author published an update. The CLI just inserts a
        # `refresh_workshop_items` job; the web worker picks it up next.
        # Idempotent — a re-fire while a refresh is already queued/running
        # is a no-op (see l4d2web/cli.py:workshop_refresh).
        'left4me-workshop-refresh': {
            'command': '/opt/left4me/.venv/bin/flask --app l4d2web.app:create_app workshop-refresh',
            'when': '*-*-* 04:00:00',
            'persistent': True,
            'user': 'left4me',
            'working_dir': '/opt/left4me/src',
            'environment_files': (
                '/etc/left4me/host.env',
                '/etc/left4me/web.env',
            ),
            'after': {
                'network-online.target',
                'left4me-web.service',
            },
        },
    },
}


# Hardening composition — proven via the hardening test plan (left4me
# commit 461b8d0). See:
#   docs/superpowers/specs/2026-05-15-hardening-threat-model.md
#   docs/superpowers/specs/2026-05-15-hardening-defenses-survey.md
#   docs/superpowers/specs/2026-05-15-hardening-test-plan.md
#   docs/superpowers/specs/2026-05-15-hardening-refactor-design.md
# (paths in the left4me repo)

# Directives both managed units take verbatim.
HARDENING_COMMON = {
    'ProtectProc': 'invisible',
    'ProcSubset': 'pid',
    'ProtectKernelTunables': 'true',
    'ProtectKernelModules': 'true',
    'ProtectKernelLogs': 'true',
    'ProtectClock': 'true',
    'ProtectControlGroups': 'true',
    'ProtectHostname': 'true',
    'LockPersonality': 'true',
    'ProtectSystem': 'strict',
    'ProtectHome': 'true',
    'PrivateTmp': 'true',
    'RestrictNamespaces': 'true',
    'RestrictRealtime': 'true',
    'RemoveIPC': 'true',
    'KeyringMode': 'private',
    'UMask': '0027',
    'RestrictAddressFamilies': 'AF_INET AF_INET6 AF_UNIX',
}

# Gameserver unit: COMMON + sudo-incompatible flags + filesystem
# virtualization + i386 amendment + per-instance PID namespace + bound
# socket binds.
HARDENING_SERVER = {
    **HARDENING_COMMON,
    'NoNewPrivileges': 'true',
    'RestrictSUIDSGID': 'true',
    'PrivateUsers': 'true',
    # PrivatePIDs is the test-plan amendment that closes D2.b: same-uid
    # ProtectProc=invisible cannot hide gunicorn from srcds (both run
    # as uid 980); a private PID namespace does.
    'PrivatePIDs': 'true',
    'PrivateIPC': 'true',
    'PrivateDevices': 'true',
    'CapabilityBoundingSet': '',
    'AmbientCapabilities': '',
    # srcds_linux is i386 (Source 2007 engine). Bare 'native' kills
    # every 32-bit syscall and traps srcds_run in a respawn loop.
    'SystemCallArchitectures': 'native x86',
    'SystemCallFilter': (
        '@system-service',
        '~@debug @mount @raw-io @reboot @swap @cpu-emulation @obsolete @privileged',
    ),
    'TemporaryFileSystem': '/var/lib /etc /opt /home /root /srv /mnt /media',
    'BindReadOnlyPaths': (
        '/var/lib/left4me/installation',
        '/var/lib/left4me/overlays',
        '/etc/left4me/host.env',
        '/etc/ssl',
        '/etc/ca-certificates',
        '/etc/resolv.conf',
        '/etc/nsswitch.conf',
        '/etc/alternatives',
    ),
    'BindPaths': '/var/lib/left4me/runtime/%i',
    # Lock srcds bindable sockets to the game port range. Hard-coded
    # range because systemd directive variable substitution is uneven.
    'SocketBindAllow': (
        'udp:27000-27999',
        'tcp:27000-27999',
    ),
    # MemoryDenyWriteExecute=true permanently excluded — Source engine
    # i386 .so files have text relocations that need mprotect(W+X)
    # during the dynamic linker's relocation pass.
}

# Web unit: COMMON + sudo-compatible additions. EXCLUDES
# NoNewPrivileges, PrivateUsers, RestrictSUIDSGID, empty
# CapabilityBoundingSet, and ~@privileged in the syscall filter — all
# sudo-incompatible until a future refactor replaces sudo with
# systemctl-managed transient units.
HARDENING_WEB = {
    **HARDENING_COMMON,
    'SystemCallArchitectures': 'native',
    'SystemCallFilter': (
        '@system-service',
        '~@debug @mount @raw-io @reboot @swap @cpu-emulation @obsolete',
    ),
}


@metadata_reactor.provides(
    'nginx/vhosts',
)
def nginx_vhosts(metadata):
    # letsencrypt/domains and monitoring/services for the vhost are auto-
    # populated by bundles/nginx/metadata.py. We just declare check_path:
    # '/health' so the auto-check hits the Flask health endpoint, not '/'.
    domain = metadata.get('left4me/domain')
    return {
        'nginx': {
            'vhosts': {
                domain: {
                    'content': 'nginx/proxy_pass.conf',
                    'context': {
                        'target': 'http://127.0.0.1:8000',
                    },
                    'check_path': '/health',
                },
            },
        },
    }


@metadata_reactor.provides(
    'nftables/input',
)
def nftables_input(metadata):
    port_start = metadata.get('left4me/port_range_start')
    port_end = metadata.get('left4me/port_range_end')
    return {
        'nftables': {
            'input': {
                f'udp dport {port_start}-{port_end} accept',
                f'tcp dport {port_start}-{port_end} accept',
            },
        },
    }


@metadata_reactor.provides(
    'systemd/units',
)
def systemd_units(metadata):
    workers = metadata.get('left4me/gunicorn_workers')
    threads = metadata.get('left4me/gunicorn_threads')

    # cgroup-v2 cpuset. `system_cpus` (set of int CPU ids, declared per
    # node) pins system/user/build; the complement pins l4d2-game. On HT
    # hosts, list both siblings of a physical core so games don't share
    # L1/L2 with system work — pairings via
    # /sys/devices/system/cpu/cpu<n>/topology/thread_siblings_list.
    vm_threads = metadata.get('vm/threads', metadata.get('vm/cores'))
    all_cpus = set(range(vm_threads))
    system_cpus = metadata.get('left4me/system_cpus')
    if not system_cpus <= all_cpus:
        raise Exception(
            f'left4me/system_cpus={sorted(system_cpus)} on {vm_threads}-thread host '
            f'includes CPUs outside [0, {vm_threads})'
        )
    game_cpus = all_cpus - system_cpus
    if not game_cpus:
        raise Exception(
            f'left4me/system_cpus={sorted(system_cpus)} on {vm_threads}-thread host '
            f'leaves no cores for games'
        )
    system_cpus_string = ','.join(str(t) for t in sorted(system_cpus))
    game_cpus_string = ','.join(str(t) for t in sorted(game_cpus))

    # Drop-in for upstream system.slice / user.slice (units we don't own).
    # Same '<parent>.d/<basename>.conf' convention as nginx and autologin.
    cpuset_dropin = {'Slice': {'AllowedCPUs': system_cpus_string}}

    return {
        'systemd': {
            'units': {
                'left4me-web.service': {
                    'Unit': {
                        'Description': 'left4me web application',
                        'After': 'network-online.target',
                        'Wants': 'network-online.target',
                    },
                    'Service': {
                        'Type': 'simple',
                        'User': 'left4me',
                        'Group': 'left4me',
                        'WorkingDirectory': '/opt/left4me/src',
                        'Environment': {
                            'HOME=/var/lib/left4me',
                            'PATH=/opt/left4me/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
                        },
                        'EnvironmentFile': (
                            '/etc/left4me/host.env',
                            '/etc/left4me/web.env',
                        ),
                        'ExecStart': (
                            '/opt/left4me/.venv/bin/gunicorn '
                            f'--workers {workers} --threads {threads} '
                            "--bind 127.0.0.1:8000 'l4d2web.app:create_app()'"
                        ),
                        'Restart': 'on-failure',
                        'RestartSec': '3',

                        # Web app writes broadly under /var/lib/left4me. Kept inline
                        # because it's web-specific (server@ uses BindPaths to bind
                        # only its instance dir).
                        'ReadWritePaths': '/var/lib/left4me',

                        # Hardening profile — see HARDENING_WEB constant near top of
                        # this file. NoNewPrivileges intentionally NOT set: workers
                        # sudo to the helpers. PrivateUsers and RestrictSUIDSGID also
                        # absent for the same reason. ProtectSystem tightens from
                        # 'full' to 'strict' via HARDENING_COMMON.
                        **HARDENING_WEB,
                    },
                    'Install': {
                        'WantedBy': {'multi-user.target'},
                    },
                },
                'left4me-server@.service': {
                    'Unit': {
                        'Description': 'left4me server instance %i',
                        'After': 'network-online.target',
                        'Wants': 'network-online.target',
                        'StartLimitBurst': '5',
                        'StartLimitIntervalSec': '60s',
                    },
                    'Service': {
                        'Type': 'simple',
                        'User': 'left4me',
                        'Group': 'left4me',
                        'EnvironmentFile': (
                            '/etc/left4me/host.env',
                            '/var/lib/left4me/instances/%i/instance.env',
                        ),
                        'WorkingDirectory': '-/var/lib/left4me/runtime/%i/merged/left4dead2',
                        'ExecStartPre': '+/usr/bin/nsenter --mount=/proc/1/ns/mnt -- /usr/local/libexec/left4me/left4me-overlay mount %i',
                        'ExecStart': '/var/lib/left4me/runtime/%i/merged/srcds_run -game left4dead2 +hostport ${L4D2_PORT} $L4D2_ARGS',
                        'ExecStopPost': '+/usr/bin/nsenter --mount=/proc/1/ns/mnt -- /usr/local/libexec/left4me/left4me-overlay umount %i',
                        'Restart': 'on-failure',
                        'RestartSec': '5',

                        # Resource control (baseline from prior performance work).
                        'Slice': 'l4d2-game.slice',
                        'Nice': '-5',
                        'IOSchedulingClass': 'best-effort',
                        'IOSchedulingPriority': '4',
                        'OOMScoreAdjust': '-200',
                        'MemoryHigh': '1.5G',
                        'MemoryMax': '2G',
                        'TasksMax': '256',
                        'LimitNOFILE': '65536',
                        'KillSignal': 'SIGINT',
                        'TimeoutStopSec': '15s',
                        'LogRateLimitIntervalSec': '0',

                        # Hardening profile — see HARDENING_SERVER constant near top of
                        # this file for per-directive rationale.
                        **HARDENING_SERVER,
                    },
                    'Install': {
                        'WantedBy': {'multi-user.target'},
                    },
                },
                'l4d2-game.slice': {
                    'Unit': {
                        'Description': 'left4me game-server slice',
                        'Before': 'slices.target',
                    },
                    'Slice': {
                        'CPUWeight': '1000',
                        'IOWeight': '1000',
                        'AllowedCPUs': game_cpus_string,
                    },
                },
                'l4d2-build.slice': {
                    'Unit': {
                        'Description': 'left4me script-sandbox build slice',
                        'Before': 'slices.target',
                    },
                    'Slice': {
                        'CPUWeight': '10',
                        'IOWeight': '10',
                        'AllowedCPUs': system_cpus_string,
                    },
                },
                'system.slice.d/99-left4me-cpuset.conf': cpuset_dropin,
                'user.slice.d/99-left4me-cpuset.conf':   cpuset_dropin,
            },
        },
    }
