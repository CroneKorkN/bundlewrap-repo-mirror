from ipaddress import ip_network, ip_interface

from bundlewrap.exceptions import NoSuchNode
from bundlewrap.metadata import atomic

repo.libs.wireguard.repo = repo


defaults = {
    'apt': {
        'packages': {
            'wireguard': {
                'backports': node.os_version < (11,),
                'triggers': [
                    'svc_systemd:systemd-networkd.service:restart',
                ],
            },
        },
    },
    'nftables': {
        'input': {
            'udp dport 51820 accept',
        },
    },
    'wireguard': {
        's2s': {},
        'clients': {},
    },
}


@metadata_reactor.provides(
    'wireguard/s2s',
    'wireguard/clients',
)
def s2s_peer_specific(metadata):
    return {
        'wireguard': {
            's2s': {
                s2s: {
                    'peer_id': repo.get_node(s2s).metadata.get(f'id'),
                    'peer_ip': repo.get_node(s2s).metadata.get(f'wireguard/my_ip'),
                    'endpoint': f'{repo.get_node(s2s).hostname}:51820',
                    'allowed_ips': [
                        str(ip_interface(repo.get_node(s2s).metadata.get(f'wireguard/my_ip')).network),
                    ],
                }
                    for s2s in metadata.get('wireguard/s2s')
            },
            'clients': {
                client: {
                    'peer_id': client,
                    'allowed_ips': [
                        str(ip_interface(conf['peer_ip']).network),
                    ],
                }
                    for client, conf in metadata.get('wireguard/clients').items()
            },
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
        'Network': {
            'DHCP': 'no',
            'IPForward': 'yes',
            'IPv6AcceptRA': 'no',
        },
    }

    for peer, config in metadata.get('wireguard/s2s').items():
        for route in config.get('allowed_ips', []):
            network.update({
                f'Route#{peer}_{route}': {
                    'Destination': route,
                    'Gateway': str(ip_interface(metadata.get('wireguard/my_ip')).ip),
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
            'PrivateKey': repo.libs.wireguard.privkey(metadata.get('id')),
            'ListenPort': 51820,
        },
    }

    for kind in ('s2s', 'clients'):
        for peer in metadata.get(f'wireguard/{kind}'):
            peer_id = metadata.get(f'wireguard/{kind}/{peer}/peer_id')
            netdev[f'WireGuardPeer#{peer}'] = {
                'PublicKey': repo.libs.wireguard.pubkey(peer_id),
                'PresharedKey': repo.libs.wireguard.psk(peer_id, metadata.get('id')),
                'AllowedIPs': ', '.join(metadata.get(f'wireguard/{kind}/{peer}/allowed_ips', [])),
                'PersistentKeepalive': 30,
            }
            endpoint = metadata.get(f'wireguard/{kind}/{peer}/endpoint', None)
            if endpoint:
                netdev[f'WireGuardPeer#{peer}']['Endpoint'] = endpoint

    return {
        'systemd': {
            'units': {
                'wireguard.netdev':  netdev,
            },
        },
    }
