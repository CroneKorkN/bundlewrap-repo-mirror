from ipaddress import ip_network, ip_interface

from bundlewrap.exceptions import NoSuchNode
from bundlewrap.metadata import atomic


defaults = {
    'apt': {
        'packages': {
            'linux-headers-amd64': {},
            'wireguard': {
                'backports': node.os_version < (11,),
                'needs': [
                    'pkg_apt:linux-headers-amd64',
                ],
                'triggers': [
                    'svc_systemd:systemd-networkd:restart',
                ],
            },
        },
    },
    'wireguard': {
        'privatekey': repo.vault.random_bytes_as_base64_for(f'{node.name} wireguard privatekey'),
    },
}


@metadata_reactor.provides(
    'systemd/units',
)
def systemd_networkd_networks(metadata):
    network = {
        'Match': {
            'Name': 'wg0',
        },
        'Address': {
            'Address': metadata.get('wireguard/my_ip'),
        },
        'Route': {
            'Destination': str(ip_interface(metadata.get('wireguard/my_ip')).network),
            'GatewayOnlink': 'yes',
            'PreferredSource': str(ip_interface(metadata.get('network/internal/ipv4')).ip),
        },
        'Network': {
            'DHCP': 'no',
            'IPForward': 'yes',
            'IPv6AcceptRA': 'no',
        },
    }

    for peer, config in metadata.get('wireguard/peers').items():
        for route in config.get('route', []):
            network.update({
                f'Route#{peer}_{route}': {
                    'Destination': route,
                    'Gateway': str(ip_interface(repo.get_node(peer).metadata.get(f'wireguard/my_ip')).ip),
                    'GatewayOnlink': 'yes',
                    'PreferredSource': str(ip_interface(metadata.get('network/internal/ipv4')).ip),
                }
            })

    return {
        'systemd': {
            'units': {
                'wireguard.network':  network,
            },
        },
    }


@metadata_reactor.provides(
    'systemd/units',
)
def systemd_networkd_netdevs(metadata):
    netdev = {
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
    
    for peer, config in metadata.get('wireguard/peers').items():
        netdev.update({
            f'WireGuardPeer#{peer}': {
                'Endpoint': config['endpoint'],
                'PublicKey': config['pubkey'],
                'PresharedKey': config['psk'],
                'AllowedIPs': ', '.join([
                    str(ip_interface(repo.get_node(peer).metadata.get(f'wireguard/my_ip')).ip),
                    *config.get('route', []),
                ]), # FIXME
                'PersistentKeepalive': 30,
            }
        })
    
    return {
        'systemd': {
            'units': {
                'wireguard.netdev':  netdev,
            },
        },
    }


@metadata_reactor.provides(
    'wireguard/peers',
)
def peer_keys(metadata):
    peers = {}

    for peer_name in metadata.get('wireguard/peers', {}):
        peer_node = repo.get_node(peer_name)
        
        first, second = sorted([node.name, peer_name])
        psk = repo.vault.random_bytes_as_base64_for(f'{first} wireguard {second}')
        
        pubkey = repo.libs.keys.get_pubkey_from_privkey(
            f'{peer_name} wireguard pubkey',
            peer_node.metadata.get('wireguard/privatekey'),
        )
        
        peers[peer_name] = {
            'psk': psk,
            'pubkey': pubkey,
            'endpoint': f'{peer_node.hostname}:51820',
        }

    return {
        'wireguard': {
            'peers': peers,
        },
    }
