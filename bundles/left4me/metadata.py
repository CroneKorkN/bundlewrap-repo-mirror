defaults = {
    'left4me': {
        'gunicorn_workers': 1,
        'gunicorn_threads': 32,
        'job_worker_threads': 4,
        'port_range_start': 27015,
        'port_range_end': 27115,
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
        },
    },
}


@metadata_reactor.provides(
    'systemd/units',
)
def systemd_units(metadata):
    workers = metadata.get('left4me/gunicorn_workers')
    threads = metadata.get('left4me/gunicorn_threads')

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
        },
    }

    return {
        'systemd': {
            'units': {
                'left4me-web.service':       web_service,
                'left4me-server@.service':   server_template,
                'l4d2-game.slice':           game_slice,
                'l4d2-build.slice':          build_slice,
            },
        },
    }
