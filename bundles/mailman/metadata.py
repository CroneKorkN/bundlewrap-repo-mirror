import base64

def derive_mailadmin_secret(metadata, salt):
    node_id = metadata.get('id')
    raw = base64.b64decode(
        repo.vault.random_bytes_as_base64_for(f'{node_id}_{salt}', length=32).value
    )
    return base64.urlsafe_b64encode(raw).rstrip(b'=').decode('ascii')


defaults = {
    'apt': {
        'packages': {
            'mailman3-full': {
                'needs': {
                    'postgres_db:mailman',
                    'postgres_role:mailman',
                    'zfs_dataset:tank/mailman',
                }
            },
            'postfix': {},
            'python3-psycopg2': {
                'needed_by': {
                    'pkg_apt:mailman3-full',
                },
            },
            'apache2': {
                'installed': False,
                'needs': {
                    'pkg_apt:mailman3-full',
                },
            },
        },
    },
    'zfs': {
        'datasets': {
            'tank/mailman': {
                'mountpoint': '/var/lib/mailman3',
            },
        },
    },
}


@metadata_reactor.provides(
    'postgresql',
    'mailman',
)
def postgresql(metadata):
    node_id = metadata.get('id')
    db_password = repo.vault.password_for(f'{node_id} database mailman')

    return {
        'postgresql': {
            'databases': {
                'mailman': {
                    'owner': 'mailman',
                },
            },
            'roles': {
                'mailman': {
                    'password': db_password,
                },
            },
        },
        'mailman': {
            'db_password': db_password,
        },
    }


@metadata_reactor.provides(
    'nginx/vhosts',
)
def nginx(metadata):
    return {
        'nginx': {
            'vhosts': {
                metadata.get('mailman/hostname'): {
                    'content': 'mailman/vhost.conf',
                },
            },
        },
    }


@metadata_reactor.provides(
    'mailman/secret_key',
)
def secret_key(metadata):
    import base64

    node_id = metadata.get('id')
    raw = base64.b64decode(
        repo.vault.random_bytes_as_base64_for(f'{node_id}_mailman_secret_key', length=32).value
    )
    secret_key = base64.urlsafe_b64encode(raw).rstrip(b'=').decode('ascii')

    return {
        'mailman': {
            'secret_key': secret_key,
        },
    }


@metadata_reactor.provides(
    'mailman',
)
def secrets(metadata):
    return {
        'mailman': {
            'web_secret': derive_mailadmin_secret(metadata, 'secret_key'),
            'api_password': derive_mailadmin_secret(metadata, 'api_password'),
            'archiver_key': derive_mailadmin_secret(metadata, 'archiver_key'),
        },
    }


@metadata_reactor.provides(
    'dns',
)
def dns(metadata):
    report_email = metadata.get('mailman/dmarc_report_email')

    return {
        'dns': {
            metadata.get('mailman/hostname'): {
                'MX': [f"5 {metadata.get('mailman/hostname')}."],
                'TXT': [
                    'v=spf1 a mx -all',
                    '; '.join(f'{k}={v}' for k, v in {
                    # dmarc version
                    'v': 'DMARC1',
                    # reject on failure
                    'p': 'reject',
                    # standard reports
                    'rua': f'mailto:{report_email}',
                    # forensic reports
                    'fo': 1,
                    'ruf': f'mailto:{report_email}',
                    # require alignment between the DKIM domain and the parent Header From domain
                    'adkim': 's',
                    # require alignment between the SPF domain (the sender) and the Header From domain
                    'aspf': 's',
                }.items())
                ],
            },
        },
    }
