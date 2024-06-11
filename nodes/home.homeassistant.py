{
    'hostname': '10.0.0.16',
    'groups': [
        'webserver',
        'backup',
        'monitored',
        'raspberry-pi',
        'autologin',
    ],
    'bundles': [
        'apt',
        'homeassistant-supervised',
        'hostname',
        'hosts',
        'htop',
        'users',
        'ssh',
        'sudo',
        'locale',
        'zsh',
        'zfs',
        'systemd',
        'systemd-timers',
        'systemd-journald',
    ],
    'metadata': {
        'id': '3d67964d-1270-4d3c-b93f-9c44219b3d59',
        'network': {
            'internal': {
                'interface': 'eth0',
                'ipv4': '10.0.0.16/24',
                'gateway4': '10.0.0.1',
            },
        },
        'apt': {
            'sources': {
                'debian': {
                    'urls': {
                        'https://deb.debian.org/debian',
                    },
                    'suites': {
                        '{codename}',
                        '{codename}-updates',
                    },
                    'components': {
                        'main',
                        'contrib',
                        'non-free',
                        'non-free-firmware',
                    },
                    'key': 'debian-{version}',
                },
                'debian-security': {
                    'urls': {
                        'http://security.debian.org/debian-security',
                    },
                    'suites': {
                        '{codename}-security',
                    },
                    'components': {
                        'main',
                        'contrib',
                        'non-free',
                        'non-free-firmware',
                    },
                    'key': 'debian-{version}-security',
                },
            },
        },
        'hosts': {
            '10.0.11.3': [
                'resolver.name',
                'secondary.resolver.name',
            ],
        },
        'letsencrypt': {
            'acme_node': 'netcup.mails',
        },
        'homeassistant': {
            'domain': 'homeassistant.ckn.li',
            'os_agent_version': '1.6.0',
        },
        'nameservers': {
            '10.0.11.3',
        },
        'users': {
            'ckn': {
                'shell': '/usr/bin/zsh',
                'authorized_keys': {
                    'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILMVroYmswD4tLk6iH+2tvQiyaMe42yfONDsPDIdFv6I ckn',
                },
            },
        },
        'sudoers': {
            'ckn': {'ALL'},
        },
        'zfs': {
            'pools': {
                'tank': {
                    'devices': [
                        '/var/lib/zfs/tank.img',
                    ],
                },
            },
        },
        'os_codename': 'bookworm',
    },
    'os': 'debian',
    'os_version': (12,),
    'pip_command': 'pip3',
}
