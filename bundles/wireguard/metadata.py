from ipaddress import ip_network, ip_interface

from bundlewrap.exceptions import NoSuchNode
from bundlewrap.metadata import atomic

repo.libs.wireguard.repo = repo

defaults = {
    'apt': {
        'packages': {
            # 'linux-headers-amd64': {},
            'wireguard': {
                'backports': node.os_version < (11,),
                # 'needs': [
                #     'pkg_apt:linux-headers-amd64',
                # ],
                'triggers': [
                    'svc_systemd:systemd-networkd:restart',
                ],
            },
        },
    },
}


@metadata_reactor.provides(
    'wireguard/privkey',
)
def privkey(metadata):
    return {
        'wireguard': {
            'privkey': repo.libs.wireguard.privkey(metadata.get('id')),
        }
    }


@metadata_reactor.provides(
    'wireguard/peers',
)
def s2s_peer_specific(metadata):
    return {
        'wireguard': {
            'peers': {
                peer: {
                    'id': repo.get_node(peer).metadata.get(f'id'),
                    'privkey': repo.get_node(peer).metadata.get(f'wireguard/privkey'),
                    'ip': repo.get_node(peer).metadata.get(f'wireguard/my_ip'),
                    'endpoint': f'{repo.get_node(peer).hostname}:51820',

                }
                    for peer in metadata.get('wireguard/peers')
            },
        },
    }


@metadata_reactor.provides(
    'wireguard/clients',
)
def client_peer_specific(metadata):
    return {
        'wireguard': {
            'clients': {
                client: {
                    'id': client,
                    'privkey': repo.libs.wireguard.privkey(client),
                }
                    for client in metadata.get('wireguard/clients')
            },
        },
    }


@metadata_reactor.provides(
    'wireguard/peers',
    'wireguard/clients',
)
def common_peer_data(metadata):
    peers = {
        'peers': {},
        'clients': {},
    }
    
    for peer_type in peers:
        for peer_name, peer_data in metadata.get(f'wireguard/{peer_type}', {}).items():
            peers[peer_type][peer_name] = {
                'psk': repo.libs.wireguard.psk(node.metadata.get('id'), peer_data['id']),
                'pubkey': repo.libs.wireguard.pubkey(peer_data['id']),
            }

    return {
        'wireguard': peers,
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

    for peer, config in {
        **metadata.get('wireguard/peers'),
        **metadata.get('wireguard/clients'),
    }.items():
        for route in config.get('route', []):
            network.update({
                f'Route#{peer}_{route}': {
                    'Destination': route,
                    'Gateway': str(ip_interface(config['ip']).ip),
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
            'PrivateKey': metadata.get('wireguard/privkey'),
            'ListenPort': 51820,
        },
    }
    
    for peer, config in {
        **metadata.get('wireguard/peers'),
        **metadata.get('wireguard/clients'),
    }.items():
        netdev.update({
            f'WireGuardPeer#{peer}': {
                'PublicKey': config['pubkey'],
                'PresharedKey': config['psk'],
                'AllowedIPs': ', '.join([
                    str(ip_interface(config['ip']).ip),
                    *config.get('route', []),
                ]), # FIXME
                'PersistentKeepalive': 30,
            }
        })
        if config.get('endpoint'):
            netdev[f'WireGuardPeer#{peer}']['Endpoint'] = config['endpoint']
    
    return {
        'systemd': {
            'units': {
                'wireguard.netdev':  netdev,
            },
        },
    }
