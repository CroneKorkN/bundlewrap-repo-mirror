defaults = {
    'php': {
        'php.ini': {
            'cgi': {
                'fix_pathinfo': '0',
            },
        },
    },
}


@metadata_reactor.provides(
    'wordpress',
)
def wordpress(metadata):
    return {
        'wordpress': {
            site: {
                'db_password': repo.vault.password_for(f"wordpress {site} db").value,
            }
                for site in metadata.get('wordpress')
        },
    }


@metadata_reactor.provides(
    'mariadb/databases',
)
def mariadb(metadata):
    return {
        'mariadb': {
            'databases': {
                site: {
                    'password': metadata.get(f'wordpress/{site}/db_password')
                }
                    for site in metadata.get('wordpress')
            },
        },
    }


@metadata_reactor.provides(
    'nginx/vhosts'
)
def vhost(metadata):
    return {
        'nginx': {
            'vhosts': {
                conf['domain']: {
                    'content': 'wordpress/vhost.conf',
                    'context': {
                        'root': f'/opt/{site}',
                    },
                }
                    for site, conf in metadata.get('wordpress').items()
            },
        },
    }


@metadata_reactor.provides(
    'zfs/datasets',
)
def zfs(metadata):
    return {
        'zfs': {
            'datasets': {
                f'tank/{site}': {
                    'mountpoint': f'/opt/{site}',
                }
                    for site in metadata.get('wordpress')
            },
        },
    }


@metadata_reactor.provides(
    'monitoring/services',
)
def check_insecure(metadata):
    return {
        'monitoring': {
            'services': {
                f'wordpress {site} insecure': {
                    'vars.command': f'/usr/lib/nagios/plugins/check_wordpress_insecure {site}',
                    'check_interval': '30m',
                    'vars.sudo': True,
                }
                    for site in metadata.get('wordpress')
            },
        },
    }
