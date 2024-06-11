defaults = {
    'apt': {
        'packages': {
            # homeassistant-supervised
            'apparmor': {},
            'bluez': {},
            'cifs-utils': {},
            'curl': {},
            'dbus': {},
            'jq': {},
            'libglib2.0-bin': {},
            'lsb-release': {},
            'network-manager': {},
            'nfs-common': {},
            'systemd-journal-remote': {},
            'systemd-resolved': {},
            'udisks2': {},
            'wget': {},
            # docker
            'docker-ce': {},
            'docker-ce-cli': {},
            'containerd.io': {},
            'docker-buildx-plugin': {},
            'docker-compose-plugin': {},
       },
        'sources': {
            # docker: https://docs.docker.com/engine/install/debian/#install-using-the-repository
            'docker': {
                'urls': {
                    'https://download.docker.com/linux/debian',
                },
                'suites': {
                    '{codename}',
                },
                'components': {
                    'stable',
                },
            },
        },
    },
    'zfs': {
        'datasets': {
            'tank/homeassistant': {
                'mountpoint': '/usr/share/hassio',
                'needed_by': {
                    'directory:/usr/share/hassio',
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
