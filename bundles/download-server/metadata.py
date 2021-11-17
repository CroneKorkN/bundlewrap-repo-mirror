defaults = {
    'users': {
        'downloads': {
            'home': '/var/lib/downloads',
            'needs': {
                'zfs_dataset:tank/downloads'
            },
        },
    },
    'zfs': {
        'datasets': {
            'tank/downloads': {
                'mountpoint': '/var/lib/downloads',
            },
        },
    },
}


@metadata_reactor.provides(
    'systemd-mount'
)
def mount_certs(metadata):
    return  {
        'systemd-mount': {
            '/var/lib/downloads_nginx': {
                'source': '/var/lib/downloads',
                'user': 'www-data',
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
                metadata.get('download-server/hostname'): {
                    'content': 'nginx/directory_listing.conf',
                    'context': {
                        'directory': '/var/lib/downloads_nginx',
                    },
                },
            },
        },
    }


@metadata_reactor.provides(
    'users/downloads/authorized_users',
)
def ssh_keys(metadata):
    return {
        'users': {
            'downloads': {
                'authorized_users': {
                    f'build-server@{other_node.name}'
                        for other_node in repo.nodes
                        if other_node.has_bundle('build-server')
                },
            },
        },
    }
