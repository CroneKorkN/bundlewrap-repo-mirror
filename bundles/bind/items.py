directories['/var/lib/bind'] = {
    'purge': True,
}

files['/etc/default/bind9'] = {
    'source': 'defaults',
}

for zone, records in node.metadata.get('bind/zones').items():
    files[f'/var/lib/bind/db.{zone}'] = {
        'source': 'db',
        'content_type': 'mako',
        'context': {
            'records': records,
        }
    }
