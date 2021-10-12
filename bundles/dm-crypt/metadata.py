defaults = {
    'apt': {
        'packages': {
            'cryptsetup': {},
        },
    },
    'dm-crypt': {},
}


@metadata_reactor.provides(
    'dm-crypt',
)
def password_from_salt(metadata):
    return {
        'dm-crypt': {
            name: { 
                'password': repo.vault.password_for(f"dm-crypt/{metadata.get('id')}/{name}"),
            }
                for name, conf in metadata.get('dm-crypt').items()
        }
    }
