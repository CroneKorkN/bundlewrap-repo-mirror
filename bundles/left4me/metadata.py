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
        # Cgroup-v2 cpuset isolation. The first `system_core_count` cores
        # (starting at 0) go to system / user / l4d2-build; the rest (up to
        # vm/threads - 1) go to l4d2-game. Bundle refuses to apply on hosts
        # with < 2 cores or when system_core_count leaves none for games.
        'system_core_count': 1,
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

    # cgroup-v2 cpuset. First `system_core_count` cores → system/user/build;
    # the rest → game. Refuse to apply if there's no useful split.
    vm_threads = metadata.get('vm/threads', metadata.get('vm/cores', 1))
    if vm_threads < 2:
        raise Exception(
            f'left4me cpu isolation needs at least 2 cores/threads, host has {vm_threads}'
        )
    system_core_count = metadata.get('left4me/system_core_count')
    game_core_count = vm_threads - system_core_count
    if system_core_count < 1 or game_core_count < 1:
        raise Exception(
            f'left4me/system_core_count={system_core_count} on {vm_threads}-thread host '
            f'leaves {game_core_count} cores for games; both must be >= 1'
        )
    system_cpus = '0' if system_core_count == 1 else f'0-{system_core_count - 1}'
    game_cpus = (
        str(system_core_count) if game_core_count == 1
        else f'{system_core_count}-{vm_threads - 1}'
    )

    web_service = {
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
    }

    server_template = {
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
    }

    game_slice = {
        'Unit': {
            'Description': 'left4me game-server slice',
            'Before': 'slices.target',
        },
        'Slice': {
            'CPUWeight': '1000',
            'IOWeight': '1000',
            'AllowedCPUs': game_cpus,
        },
    }

    build_slice = {
        'Unit': {
            'Description': 'left4me script-sandbox build slice',
            'Before': 'slices.target',
        },
        'Slice': {
            'CPUWeight': '10',
            'IOWeight': '10',
            'AllowedCPUs': system_cpus,
        },
    }

    units = {
        'left4me-web.service':       web_service,
        'left4me-server@.service':   server_template,
        'l4d2-game.slice':           game_slice,
        'l4d2-build.slice':          build_slice,
    }
    # Drop-ins on the upstream system.slice / user.slice (units we don't
    # own). Same '<parent>.d/<basename>.conf' convention as nginx and
    # autologin use elsewhere in this repo.
    cpuset_dropin = {'Slice': {'AllowedCPUs': system_cpus}}
    units['system.slice.d/99-left4me-cpuset.conf'] = cpuset_dropin
    units['user.slice.d/99-left4me-cpuset.conf'] = cpuset_dropin

    return {
        'systemd': {
            'units': units,
        },
    }
