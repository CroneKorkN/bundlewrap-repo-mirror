from ipaddress import ip_interface


defaults = {
    'apt': {
        'packages': {
            'jq': {},
            'ethtool': {},
            'net-tools': {},
        },
    },
    'systemd': {
        'units': {
            'wakeonlan-remove-downtime.service': {
                'Unit': {
                    'Description': 'remove icinga downtime after wakeup',
                    'After': {
                        'network-online.target',
                        'suspend.target',
                    },
                },
                'Service': {
                    'ExecStart': '/usr/local/bin/downtime remove',
                },
                'Install': {
                    'WantedBy': {
                        'suspend.target',
                    },
                },
            },
        },
    },
    'systemd-timers': {
        'suspend-if-idle': {
            'command': f'suspend_if_idle',
            'when': 'minutely',
            'success_exit_status': '75',
            'env': {
                'THIS_SERVICE': 'suspend-if-idle.service',
            },
        },
    },
}


@metadata_reactor.provides(
    'wol-sleeper/mac',
    'wol-sleeper/wake_command',
)
def wake_command(metadata):
    waker_hostname = repo.get_node(metadata.get('wol-sleeper/waker')).hostname
    mac = metadata.get(f"network/{metadata.get('wol-sleeper/network')}/mac")
    ip = ip_interface(metadata.get(f"network/{metadata.get('wol-sleeper/network')}/ipv4")).ip

    return {
        'wol-sleeper': {
            'mac': mac,
            'wake_command': f"ssh -o StrictHostKeyChecking=no wol@{waker_hostname} '/usr/bin/wakeonlan {mac}' && while ! ping {ip} -c1 -W3; do true; done",
        },
    }


@metadata_reactor.provides(
    'systemd/units/wakeonline-setup.service',
    'systemd/services/wakeonline-setup.service',
)
def systemd(metadata):
    interface = metadata.get(f"network/{metadata.get('wol-sleeper/network')}/interface")

    return {
        'systemd': {
            'units': {
                'wakeonline-setup.service': {
                    'Unit': {
                        'After': 'network.target',
                    },
                    'Service': {
                        'Type': 'oneshot',
                        'RemainAfterExit': 'yes',
                        'ExecStart': f'ethtool -s {interface} wol g',
                    },
                },
            },
            'services': {
                'wakeonline-setup.service': {},
            },
        },
    }
