from ipaddress import ip_interface

defaults = {
    'systemd': {
        'units': {
            'build-server.service': {
                'Unit': {
                    'Description': 'build server',
                    'After': 'network.target',
                },
                'Service': {
                    'User': 'build-server',
                    'Group': 'build-server',
                    'Environment': 'STRATEGIES_DIR=/opt/build-server/strategies',
                    'ExecStart': '/opt/build-server/build-server-crystal --port 4000',
                    'Restart': 'always',
                },
                'Install': {
                    'WantedBy': {'multi-user.target'},
                },
            },
        },
    },
    'users': {
        'build-server': {
            'home': '/var/lib/build-server',
        },
    },
}


@metadata_reactor.provides(
    'build-server',
)
def agent_conf(metadata):
    download_server = repo.get_node(metadata.get('build-server/download_server'))
    return {
        'build-server': {
            'architectures': {
                architecture: {
                    'ip': str(ip_interface(repo.get_node(conf['node']).metadata.get('network/internal/ipv4')).ip),
                }
                    for architecture, conf in metadata.get('build-server/architectures').items()
            },
            'download_server_ip': str(ip_interface(download_server.metadata.get('network/internal/ipv4')).ip),
        },
    }


@metadata_reactor.provides(
    'nginx/vhosts',
)
def nginx(metadata):
    return {
        'nginx': {
            'vhosts': {
                metadata.get('build-server/hostname'): {
                    'content': 'nginx/proxy_pass.conf',
                    'context': {
                        'target': 'http://127.0.0.1:4000',
                    },
                },
            },
        },
    }
