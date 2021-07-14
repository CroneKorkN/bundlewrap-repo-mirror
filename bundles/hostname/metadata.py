hostname = '.'.join([*reversed(node.name.split('.')), 'ckn', 'li'])

defaults = {
    'hostname': hostname,
    'hosts': {
        '127.0.0.1': [hostname],
    },
}


@metadata_reactor.provides(
    'dns',
)
def dns(metadata):
    return {
        'dns': {
            metadata.get('hostname'): repo.libs.dns.get_a_records(metadata, external=False),
        },
    }
