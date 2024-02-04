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
