from ipaddress import ip_network

from bundlewrap.exceptions import NoSuchNode
from bundlewrap.metadata import atomic


defaults = {
    'apt': {
        'packages': {
            'wireguard': {},
        },
    },
    'wireguard': {
        'privatekey': repo.libs.keys.gen_privkey(repo, f'{node.name} wireguard privatekey'),
    },
}


@metadata_reactor.provides(
    'wireguard/peers',
)
def peer_psks(metadata):
    peers = {}

    for peer_name in metadata.get('wireguard/peers', {}):
        peers[peer_name] = {}

        if node.name < peer_name:
            peers[peer_name] = {
                'psk': repo.vault.random_bytes_as_base64_for(f'{node.name} wireguard {peer_name}'),
            }
        else:
            peers[peer_name] = {
                'psk': repo.vault.random_bytes_as_base64_for(f'{peer_name} wireguard {node.name}'),
            }

    return {
        'wireguard': {
            'peers': peers,
        },
    }


@metadata_reactor.provides(
    'wireguard/peers',
)
def peer_pubkeys(metadata):
    peers = {}

    for peer_name in metadata.get('wireguard/peers', {}):
        try:
            rnode = repo.get_node(peer_name)
        except NoSuchNode:
            continue

        peers[peer_name] = {
            'pubkey': repo.libs.keys.get_pubkey_from_privkey(
                repo,
                f'{rnode.name} wireguard pubkey',
                rnode.metadata.get('wireguard/privatekey'),
            ),
        }

    return {
        'wireguard': {
            'peers': peers,
        },
    }


@metadata_reactor.provides(
    'wireguard/peers',
)
def peer_ips_and_endpoints(metadata):
    peers = {}

    for peer_name in metadata.get('wireguard/peers', {}):
        try:
            rnode = repo.get_node(peer_name)
        except NoSuchNode:
            continue

        ips = rnode.metadata.get('wireguard/subnets', set())
        ips.add(rnode.metadata.get('wireguard/my_ip').split('/')[0])
        ips = repo.libs.tools.remove_more_specific_subnets(ips)

        peers[rnode.name] = {
            'endpoint': '{}:51820'.format(rnode.metadata.get('wireguard/external_hostname', rnode.hostname)),
            'ips': ips,
        }

    return {
        'wireguard': {
            'peers': peers,
        },
    }


@metadata_reactor.provides(
    'interfaces/wg0/ips',
)
def interface_ips(metadata):
    return {
        'interfaces': {
            'wg0': {
                'ips': {
                    metadata.get('wireguard/my_ip'),
                },
            },
        },
    }


@metadata_reactor.provides(
    'interfaces/wg0/routes',
)
def routes(metadata):
    network = ip_network(metadata.get('wireguard/my_ip'), strict=False)
    ips = {
        f'{network.network_address}/{network.prefixlen}',
    }
    routes = {}

    for _, peer_config in metadata.get('wireguard/peers', {}).items():
        for ip in peer_config['ips']:
            ips.add(ip)

    if '0.0.0.0/0' in ips:
        ips.remove('0.0.0.0/0')

    for ip in repo.libs.tools.remove_more_specific_subnets(ips):
        routes[ip] = {}

    return {
        'interfaces': {
            'wg0': {
                'routes': routes,
            },
        },
    }
