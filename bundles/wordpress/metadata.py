defaults = {
    'wordpress': {},
}


@metadata_reactor.provides(
    'wordpress',
)
def wordpress(metadata):
    return {
        'wordpress': {
            domain: {
                'root': f'/var/www/{domain}',
            }
                for domain in metadata.get('wordpress')
        },
    }


@metadata_reactor.provides(
    'postgresql/roles',
    'postgresql/databases',
)
def postgresql(metadata):
    return {
        'postgresql': {
            'roles': {
                domain: {
                    'password': repo.vault.password_for(f'{node.name} postgresql wordpress {domain}').value,
                }
                    for domain in metadata.get('wordpress')
            },
            'databases': {
                domain: {
                    'owner': domain,
                }
                    for domain in metadata.get('wordpress')
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
                domain: {
                    'content': 'wordpress/vhost.conf',
                    'context': {
                        'root': conf['root'],
                    },
                    'internal_dns': conf.get('internal_dns', True)
                }
                    for domain, conf in metadata.get('wordpress').items()
            },
        },
    }
