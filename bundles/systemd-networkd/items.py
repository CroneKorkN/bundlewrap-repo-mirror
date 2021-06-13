assert node.has_bundle('systemd')

from bundlewrap.exceptions import BundleError


files = {
    '/etc/network/interfaces': {
        'delete': True,
    },
}

if node.metadata.get('systemd-networkd/enable-resolved', False):
    symlinks['/etc/resolv.conf'] = {
        'target': '/run/systemd/resolve/stub-resolv.conf',
    }
    svc_systemd['systemd-resolved'] = {}
else:
    files['/etc/resolv.conf'] = {
        'content_type': 'mako',
    }


directories = {
    '/etc/systemd/network': {
        'purge': True,
    },
}

mac_host_prefix = '%04x' % (node.magic_number % 65534)
generated_mac = f'52:54:00:{mac_host_prefix[0:2]}:{mac_host_prefix[2:4]}:{{}}'

# Don't use .get() here. We might end up with a node without a network
# config!
for interface, config in node.metadata['interfaces'].items():
    if config.get('dhcp', False):
        if 'vlans' in config:
            raise BundleError(f'{node.name} interface {interface} cannot use vlans and dhcp!')
        template = 'template-iface-dhcp.network'
    else:
        template = 'template-iface-nodhcp.network'

    if '.' in interface:
        vlan_id = int(interface.split('.')[1])
        vlan_hex = '%02x' % (vlan_id % 255)
        files['/etc/systemd/network/60-iface-{}.netdev'.format(interface)] = {
            'source': 'template-iface-vlan.netdev',
            'content_type': 'mako',
            'context': {
                'interface': interface,
                'vlan': vlan_id,
                'mac': generated_mac.format(vlan_hex)
            },
            'needed_by': {
                'svc_systemd:systemd-networkd',
            },
            'triggers': {
                'svc_systemd:systemd-networkd:restart',
            },
        }
        weight = 61
    else:
        weight = 50

    if not config.get('ignore', False):
        files['/etc/systemd/network/{}-iface-{}.network'.format(weight, interface)] = {
            'source': template,
            'content_type': 'mako',
            'context': {
                'interface': interface,
                'config': config,
            },
            'needed_by': {
                'svc_systemd:systemd-networkd',
            },
            'triggers': {
                'svc_systemd:systemd-networkd:restart',
            },
        }

for bond, config in node.metadata.get('systemd-networkd/bonds', {}).items():
    files['/etc/systemd/network/20-bond-{}.netdev'.format(bond)] = {
        'source': 'template-bond.netdev',
        'content_type': 'mako',
        'context': {
            'bond': bond,
            'mode': config.get('mode', '802.3ad'),
            'prio': config.get('priority', '32768'),
        },
        'needed_by': {
            'svc_systemd:systemd-networkd',
        },
        'triggers': {
            'svc_systemd:systemd-networkd:restart',
        },
    }
    files['/etc/systemd/network/21-bond-{}.network'.format(bond)] = {
        'source': 'template-bond.network',
        'content_type': 'mako',
        'context': {
            'bond': bond,
            'match': config['match'],
        },
        'needed_by': {
            'svc_systemd:systemd-networkd',
        },
        'triggers': {
            'svc_systemd:systemd-networkd:restart',
        },
    }

for brname, config in node.metadata.get('systemd-networkd/bridges', {}).items():
    files['/etc/systemd/network/30-bridge-{}.netdev'.format(brname)] = {
        'source': 'template-bridge.netdev',
        'content_type': 'mako',
        'context': {
            'bridge': brname,
        },
        'needed_by': {
            'svc_systemd:systemd-networkd',
        },
        'triggers': {
            'svc_systemd:systemd-networkd:restart',
        },
    }
    files['/etc/systemd/network/31-bridge-{}.network'.format(brname)] = {
        'source': 'template-bridge.network',
        'content_type': 'mako',
        'context': {
            'bridge': brname,
            'match': config['match'],
        },
        'needed_by': {
            'svc_systemd:systemd-networkd',
        },
        'triggers': {
            'svc_systemd:systemd-networkd:restart',
        },
    }

svc_systemd = {
    'systemd-networkd': {},
}
