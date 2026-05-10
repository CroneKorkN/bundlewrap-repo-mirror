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
            'EnvironmentFile': {
                '/etc/left4me/host.env',
                '/etc/left4me/web.env',
            },
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

    return {
        'systemd': {
            'units': {
                'left4me-web.service': web_service,
            },
        },
    }
