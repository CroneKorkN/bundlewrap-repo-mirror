from ipaddress import ip_interface

database_password = repo.vault.password_for(f'{node.name} db mailserver')

defaults = {
    'mailserver': {
        'maildir': '/var/vmail',
        'database': {
            'host': '127.0.0.1', # dont use localhost
            'name': 'mailserver',
            'user': 'mailserver',
            'password': database_password,
        },
        'test_password': repo.vault.password_for(f'{node.name} test_pw mailserver'),
        'domains': [],
    },
    'postgresql': {
        'roles': {
            'mailserver': {
                'password': database_password,
            },
        },
        'databases': {
            'mailserver': {
                'owner': 'mailserver',
            },
        },
    },
    'zfs': {
        'datasets': {
            'tank/vmail': {
                'mountpoint': '/var/vmail',
                'compression': 'on',
            },
        },
    },
}


@metadata_reactor.provides(
    'dns',
)
def dns(metadata):
    dns = {}
    
    for domain in metadata.get('mailserver/domains'):
        dns[domain] = {
            'MX': [domain],
            'TXT': ['v=spf1 a mx -all'],
        }

    return {
        'dns': dns,
    }

@metadata_reactor.provides(
    'letsencrypt/domains',
)
def letsencrypt(metadata):
    return {
        'letsencrypt': {
            'domains': {
                metadata.get('mailserver/hostname'): set(),
            },
        },
    } 
