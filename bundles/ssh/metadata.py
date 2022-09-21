from ipaddress import ip_interface
from base64 import b64decode

defaults = {
    'ssh': {
        'multiplex_incoming': True,
    },
}


@metadata_reactor.provides(
    'ssh/allow_users',
)
def users(metadata):
    return {
        'ssh': {
            'allow_users': set(
                name
                    for name, conf in metadata.get('users').items()
                    if conf.get('authorized_keys', []) or conf.get('authorized_users', [])
            ),
        },
    }


@metadata_reactor.provides(
    'ssh/host_key',
)
def host_key(metadata):
    private, public = repo.libs.ssh.generate_ed25519_key_pair(
        b64decode(str(repo.vault.random_bytes_as_base64_for(f"HostKey {metadata.get('id')}", length=32)))
    )

    return {
        'ssh': {
            'host_key': {
                'private': private + '\n',
                'public': public + f' root@{node.name}',
            }
        },
    }


@metadata_reactor.provides(
    'ssh/hostnames',
)
def hostnames(metadata):
    ips = set()

    for network in node.metadata.get('network').values():
        if network.get('ipv4', None):
            ips.add(str(ip_interface(network['ipv4']).ip))
        if network.get('ipv6', None):
            ips.add(str(ip_interface(network['ipv6']).ip))

    domains = {
        domain
            for domain, records in node.metadata.get('dns').items()
            for type, values in records.items()
            if type in {'A', 'AAAA'}
            and set(values) & ips
    }

    return {
        'ssh': {
            'hostnames': {
                node.hostname,
                *ips,
                *domains,
            }
        },
    }
