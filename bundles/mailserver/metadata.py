from ipaddress import ip_interface

database_password = repo.vault.password_for(f'{node.name} db mailserver')

defaults = {
    'mailserver': {
        'debug': False,
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
                'atime': 'off',
                'recordsize': '16K',
            },
            'tank/vmail/index': {
                'mountpoint': '/var/vmail/index',
                'compression': 'on',
                'atime': 'off',
                'recordsize': '4K',
                'com.sun:auto-snapshot': 'false',
                'backup': False,
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
            'MX': [f"5 {metadata.get('mailserver/hostname')}."],
            'TXT': ['v=spf1 a mx -all'],
        }
        report_email = metadata.get('mailserver/dmarc_report_email')
        dns[f'_dmarc.{domain}'] = {
            'TXT': ['; '.join(f'{k}={v}' for k, v in {
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
            }.items())]
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
                metadata.get('mailserver/hostname'): {
                    'reload': {'dovecot', 'postfix'},
                },
            },
        },
    }
