from ipaddress import ip_interface

defaults = {
    'flask': {
        'build-server' : {
            'git_url': "https://git.sublimity.de/cronekorkn/build-server.git",
            'port': 4000,
            'app_module': 'build_server',
            'user': 'build-server',
            'group': 'build-server',
            'timeout': 900,
            'env': {
                'CONFIG': '/etc/build-server.json',
                'STRATEGIES_DIR': '/opt/build-server/strategies',
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
    'build-server',
)
def ci(metadata):
    return {
        'build-server': {
            'ci': {
                f'{repo}@{other_node.name}': {
                    'hostname': other_node.metadata.get('hostname'),
                    'repo': repo,
                    **options,
                }
                    for other_node in repo.nodes
                    if other_node.has_bundle('build-ci')
                    for repo, options in other_node.metadata.get('build-ci').items()
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
                metadata.get('build-server/hostname'): {
                    'content': 'nginx/proxy_pass.conf',
                    'context': {
                        'target': 'http://127.0.0.1:4000',
                    },
                },
            },
        },
    }
