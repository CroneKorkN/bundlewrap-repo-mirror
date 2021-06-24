from ipaddress import ip_network, ip_interface

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
    'systemd-networkd/networks',
)
def systemd_networkd_networks(metadata):
    return {
        'systemd-networkd': {
            'networks': {
                'wg0': {
                    'Match': {
                        'Name': 'wg0',
                    },
                    'Address': {
                        'Address': metadata.get('wireguard/my_ip'),
                    },
                    'Route': {
                        'Destination': str(ip_interface(metadata.get('wireguard/my_ip')).network),
                        'GatewayOnlink': 'yes',
                    },
                    'Network': {
                        'DHCP': 'no',
                        'IPv6AcceptRA': 'no',
                    },
                },
            },
        },
    }


@metadata_reactor.provides(
    'systemd-networkd/netdevs',
)
def systemd_networkd_netdevs(metadata):
    wg0 = {
        'NetDev': {
            'Name': 'wg0',
            'Kind': 'wireguard',
            'Description': 'WireGuard server',
        },
        'WireGuard': {
            'PrivateKey': metadata.get('wireguard/privatekey'),
            'ListenPort': 51820,
        },
    }
    
    for name, config in metadata.get('wireguard/peers').items():
        wg0.update({
            f'WireGuardPeer#{name}': {
                'Endpoint': config['endpoint'],
                'PublicKey': config['pubkey'],
                'PresharedKey': config['psk'],
                'AllowedIPs': '0.0.0.0/0', # FIXME
                'PersistentKeepalive': 30,
            }
        })
    
    return {
        'systemd-networkd': {
            'netdevs': {
                'wg0': wg0,
            },
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
