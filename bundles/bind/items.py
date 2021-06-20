directories['/var/lib/bind'] = {
    'purge': True,
}

files['/etc/default/bind9'] = {
    'source': 'defaults',
}

def column_width(column, table):
    return max(map(lambda row: len(row[column]), table)) if table else 0

for zone, records in node.metadata.get('bind/zones').items():
    files[f'/var/lib/bind/db.{zone}'] = {
        'source': 'db',
        'content_type': 'mako',
        'context': {
            'records': records,
            'column_width': column_width,
        }
    }
