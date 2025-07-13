from ipaddress import ip_interface
from base64 import b64decode

defaults = {
    'ssh': {
        'multiplex_incoming': True,
        'is_known_as': set(), # known_hosts for other nodes
        'known_hosts': set(), # known_hosts for this node
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
                'public': f'{public} {node.name}',
            }
        },
    }


@metadata_reactor.provides(
    'ssh/hostnames',
)
def hostnames(metadata):
    ips = set()

    for network in metadata.get('network').values():
        if network.get('ipv4', None):
            ips.add(str(ip_interface(network['ipv4']).ip))
        if network.get('ipv6', None):
            ips.add(str(ip_interface(network['ipv6']).ip))

    domains = {
        domain
            for domain, records in metadata.get('dns').items()
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


@metadata_reactor.provides(
    'ssh/is_known_as',
)
def is_known_as(metadata):
    return {
        'ssh': {
            'is_known_as': repo.libs.ssh.known_hosts_entry_for(
                node_id=metadata.get('id'),
                hostnames=tuple(sorted(metadata.get('ssh/hostnames'))),
                pubkey=metadata.get('ssh/host_key/public'),
            ),
        },
    }


@metadata_reactor.provides(
    'ssh/known_hosts',
)
def known_hosts(metadata):
    return {
        'ssh': {
            'known_hosts': set(
                line
                    for other_node in repo.nodes
                    if other_node != node
                    and other_node.has_bundle('ssh')
                    for line in other_node.metadata.get('ssh/is_known_as')
            )
        }
    }
