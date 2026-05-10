assert node.has_bundle('nftables')
assert node.has_bundle('systemd')


defaults = {
    'left4me': {
        # Application-wide defaults; node only overrides if it really needs to.
        'git_url': 'https://git.sublimity.de/cronekorkn/left4me.git',
        'git_branch': 'master',
        'secret_key': repo.vault.random_bytes_as_base64_for(f'{node.name} left4me secret_key', length=32).value,
        'gunicorn_workers': 1,
        'gunicorn_threads': 32,
        'job_worker_threads': 4,
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
                        # NoNewPrivileges intentionally NOT set: workers sudo to the helpers.
                        'ProtectSystem': 'full',
                        'ReadWritePaths': '/var/lib/left4me',
                        'PrivateTmp': 'true',
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
                        'ExecStartPre': (
                            '+/usr/bin/nsenter --mount=/proc/1/ns/mnt -- '
                            '/usr/local/libexec/left4me/left4me-overlay mount %i'
                        ),
                        'ExecStart': (
                            '/var/lib/left4me/runtime/%i/merged/srcds_run '
                            '-game left4dead2 +hostport ${L4D2_PORT} $L4D2_ARGS'
                        ),
                        'ExecStopPost': (
                            '+/usr/bin/nsenter --mount=/proc/1/ns/mnt -- '
                            '/usr/local/libexec/left4me/left4me-overlay umount %i'
                        ),
                        'Restart': 'on-failure',
                        'RestartSec': '5',
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
                        'NoNewPrivileges': 'true',
                        'PrivateTmp': 'true',
                        'PrivateDevices': 'true',
                        'ProtectHome': 'true',
                        'ProtectSystem': 'strict',
                        'ReadOnlyPaths': '/var/lib/left4me/installation /var/lib/left4me/overlays',
                        'ReadWritePaths': '/var/lib/left4me/runtime/%i',
                        'RestrictSUIDSGID': 'true',
                        'LockPersonality': 'true',
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
