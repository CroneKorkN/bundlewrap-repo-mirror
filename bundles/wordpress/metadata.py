defaults = {}


@metadata_reactor.provides(
    'wordpress',
)
def wordpress(metadata):
    return {
        'wordpress': {
            site: {
                'db_password': repo.vault.password_for(f"wordpress {site} db").value,
            }
                for site in metadata.get('wordpress', {})
        },
    }


@metadata_reactor.provides(
    'mariadb',
)
def mariadb(metadata):
    return {
        'mariadb': {
            'databases': {
                site: {
                    'password': metadata.get(f'wordpress/{site}/db_password')
                }
                    for site in metadata.get('wordpress', {})
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
