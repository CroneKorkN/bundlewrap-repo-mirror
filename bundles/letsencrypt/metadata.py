from ipaddress import ip_interface

defaults = {
    'apt': {
        'packages': {
            'dehydrated': {},
            'dnsutils': {},
        },
    },
    'letsencrypt': {
        'domains': {
            # 'example.com': {
            #     'aliases': {'www.example.com'},
            #     'reload': {'nginx'},
            #     'owner': 'www-data',
            #     'location': '/opt/app/certs',
            # },
        },
    },
}
