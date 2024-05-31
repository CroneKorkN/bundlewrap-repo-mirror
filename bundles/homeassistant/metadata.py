defaults = {
    'apt': {
        'packages': {
            'python3': {},
            'python3-dev': {},
            'python3-pip': {},
            'python3-venv': {},
            'libffi-dev': {},
            'libssl-dev': {},
            'libjpeg-dev': {},
            'zlib1g-dev': {},
            'autoconf': {},
            'build-essential': {},
            'libopenjp2-7': {},
            'libturbojpeg0-dev': {},
            'tzdata': {},
            'bluez': {},
            'libtiff6': {},
            'ffmpeg': {},
            'liblapack3': {},
            'liblapack-dev': {},
            'libatlas-base-dev': {},
            'libpcap-dev': {},
        },
    },
    'systemd': {
        'units': {
            f'homeassistant.service': {
                'Unit': {
                    'Description': "Home Assstant",
                    'After': 'network.target',
                },
                'Service': {
                    'User': 'homeassistant',
                    'Group': 'homeassistant',
                    'WorkingDirectory': "/opt/homeassistant",
                    'ExecStart': "/opt/homeassistant/venv/bin/python3 /opt/homeassistant/venv/bin/hass -c /opt/homeassistant/data",
                },
                'Install': {
                    'WantedBy': {
                        'multi-user.target'
                    },
                },
            }
        },
    },
    'zfs': {
        'datasets': {
            'tank/homeassistant': {
                'mountpoint': '/opt/homeassistant/data',
                'needed_by': {
                    'user:homeassistant',
                    'directory:/opt/homeassistant',
                },
            },
        },
    },
}


@metadata_reactor.provides(
    'nginx/vhosts',
)
def nginx(metadata):
    return {
        'nginx': {
            'vhosts': {
                metadata.get('homeassistant/domain'): {
                    'content': 'homeassistant/vhost.conf',
                },
            },
        },
    }
