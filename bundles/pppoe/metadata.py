defaults = {
    'apt': {
        'packages': {
            'pppoe': {},
        },
    },
    'modules-load': {
        'pppoe',
        'pppox',
        'ppp_generic',
        'sch_cake',
    },
    'nftables': {
        # sorted before the port accepts, so nothing on the router is reachable from the internet;
        # wireguard to htz.mails is initiated from here and passes as established
        'input': {
            'iifname ppp0 drop',
        },
        'forward': {
            'iifname ppp0 ct state new drop',
            # pppoe has an mtu of 1492
            'oifname ppp0 tcp flags syn tcp option maxseg size set rt mtu',
        },
        'nat': {
            'oifname ppp0 masquerade',
        },
    },
    'systemd': {
        'units': {
            'pppoe-isp.service': {
                'Unit': {
                    'Description': 'PPPoE Internet Connection',
                    'BindsTo': 'sys-subsystem-net-devices-external.device',
                    'After': 'sys-subsystem-net-devices-external.device',
                },
                'Service': {
                    # pppd exits when the link drops, systemd redials
                    'Type': 'notify',
                    'ExecStart': '/usr/sbin/pppd call isp nodetach up_sdnotify',
                    'Restart': 'always',
                    'RestartSec': 5,
                },
            },
            # pppd only dials, networkd configures the link it creates
            'ppp0.network': {
                'Match': {
                    'Name': 'ppp0',
                },
                'Link': {
                    'RequiredForOnline': 'no',
                },
                'Network': {
                    # keep the address set by pppd
                    'KeepConfiguration': 'yes',
                    'LinkLocalAddressing': 'no',
                    'IPv6AcceptRA': 'no',
                },
                'Route': {
                    'Destination': '0.0.0.0/0',
                },
                'CAKE': {
                    # - no drops save
                    # - bis 37MBit keine retries bei: iperf3 --client 49.12.184.229 -t999 -i5 --bidir
                    'Bandwidth': '37M',
                    'RTTSec': '100ms',
                    'PriorityQueueingPreset': 'besteffort',
                    'FlowIsolationMode': 'triple',
                    'NAT': 'yes',
                },
            },
        },
    },
}
