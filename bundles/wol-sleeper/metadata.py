from ipaddress import ip_interface


defaults = {
    'apt': {
        'packages': {
            'jq': {},
            'ethtool': {},
            'net-tools': {},
        },
    },
}


@metadata_reactor.provides(
    'systemd-timers/suspend-if-idle',
)
def timer(metadata):
    return {
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
    'wol-sleeper/wake_command',
)
def wake_command(metadata):
    waker_hostname = repo.get_node(metadata.get('wol-sleeper/waker')).hostname
    mac = metadata.get(f"network/{metadata.get('wol-sleeper/network')}/mac")
    ip = ip_interface(metadata.get(f"network/{metadata.get('wol-sleeper/network')}/ipv4")).ip

    return {
        'wol-sleeper': {
            'wake_command': f"ssh -o StrictHostKeyChecking=no wol@{waker_hostname} 'wakeonlan {mac} && while ! ping {ip} -c1 -W3; do true; done'",
        },
    }


@metadata_reactor.provides(
    'systemd/units/enable-wol.service',
    'systemd/services/enable-wol.service',
)
def systemd(metadata):
    interface = metadata.get(f"network/{metadata.get('wol-sleeper/network')}/interface")

    return {
        'systemd': {
            'units': {
                'enable-wol.service': {
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
                'enable-wol.service': {},
            },
        },
    }
