defaults = {
    'hostname': '.'.join([*reversed(node.name.split('.')), 'ckn', 'li']),
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
