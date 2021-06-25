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
        'privatekey': repo.vault.random_bytes_as_base64_for(f'{node.name} wireguard privatekey'),
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
                        'IPForward': 'yes',
                        'IPMasquerade': 'yes',
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
