routeros['/ip/dns'] = {
    'servers': '8.8.8.8',
}

routeros['/system/identity'] = {
    'name': node.name,
}

# for service in (
#     'api-ssl',  # slow :(
#     'ftp',  # we can download files via HTTP
#     'telnet',
#     'www-ssl',  # slow :(
#     'winbox',
# ):
#     routeros[f'/ip/service?name={service}'] = {
#         'disabled': True,
#     }

# LOGGING_TOPICS = (
#     'critical',
#     'error',
#     'info',
#     'stp',
#     'warning',
# )
# for topic in LOGGING_TOPICS:
#     routeros[f'/system/logging?action=memory&topics={topic}'] = {}

# routeros['/snmp'] = {
#     'enabled': True,
# }
# routeros['/snmp/community?name=public'] = {
#     'addresses': '0.0.0.0/0',
#     'disabled': False,
#     'read-access': True,
#     'write-access': False,
# }

# routeros['/system/clock'] = {
#     'time-zone-autodetect': False,
#     'time-zone-name': 'UTC',
# }

# routeros['/ip/neighbor/discovery-settings'] = {
#     'protocol': 'cdp,lldp,mndp',
# }

# routeros['/ip/route?dst-address=0.0.0.0/0'] = {
#     'gateway': node.metadata.get('routeros/gateway'),
# }

for vlan_name, vlan_id in node.metadata.get('routeros/vlans').items():
    routeros[f'/interface/vlan?name={vlan_name}'] = {
        'vlan-id': vlan_id,
        'interface': 'bridge',
        'tags': {
            'routeros-vlan',
        },
        'needs': {
            #'routeros:/interface/bridge?name=bridge',
        },
    }

    routeros[f"/interface/bridge/vlan?vlan-ids={vlan_id}"] = {
        'bridge': 'bridge',
        'untagged': sorted(node.metadata.get(f'routeros/vlan_ports/{vlan_name}/untagged')),
        'tagged': sorted(node.metadata.get(f'routeros/vlan_ports/{vlan_name}/tagged')),
        '_comment': vlan_name,
        'tags': {
            'routeros-vlan-ports',
        },
        'needs': {
            #'routeros:/interface/bridge?name=bridge',
            'tag:routeros-vlan',
        },
    }

# create IPs
for ip, ip_conf in node.metadata.get('routeros/ips').items():
    routeros[f'/ip/address?address={ip}'] = {
        'interface': ip_conf['interface'],
        'tags': {
            'routeros-ip',
        },
        'needs': {
            'tag:routeros-vlan',
        },
    }

routeros['/interface/bridge?name=bridge'] = {
    'vlan-filtering': True, # ENABLE AFTER PORT VLANS ARE SET UP
    'igmp-snooping': False,
    'priority': node.metadata.get('routeros/bridge_priority'),
    'protocol-mode': 'rstp',
    'needs': {
        'tag:routeros-vlan',
        'tag:routeros-vlan-ports',
        'tag:routeros-ip',
    },
}

# purge unused vlans
routeros['/interface/vlan'] = {
    'purge': {
        'id-by': 'name',
    },
    'needed_by': {
        'tag:routeros-vlan',
    }
}

routeros['/interface/bridge/vlan'] = {
    'purge': {
        'id-by': 'vlan-ids',
        'keep': {
            'dynamic': True,
        },
    },
    'needed_by': {
        'tag:routeros-vlan',
    }
}
