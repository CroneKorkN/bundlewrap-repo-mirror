h = repo.libs.hashable.hashable

defaults = {
    'apt': {
        'packages': {
            'snmp': {},
            'snmp-mibs-downloader': {},
        },
    },
}


@metadata_reactor.provides(
    'telegraf/config/inputs/snmp',
)
def routeros_monitoring_telegraf_inputs(metadata):
    return {
        "telegraf": {
            "config": {
                "inputs": {
                    "snmp": {
                        h({
                            "agents": [f"udp://{routeros_node.hostname}:161"],
                            "version": 2,
                            "community": "public",
                            "interval": "30s",
                            "tags": {
                                "host": routeros_node.name,
                                "operating_system": "routeros",
                            },

                            # scalar -> input-level
                            "field": [
                                {
                                    "name": "switch_name",
                                    "oid": "SNMPv2-MIB::sysName.0",
                                    "is_tag": True,
                                },
                                # MikroTik Health (scalars)
                                {
                                    "name": "hw_voltage",
                                    "oid": "MIKROTIK-MIB::mtxrHlVoltage",
                                },
                                {
                                    "name": "hw_temp",
                                    "oid": "MIKROTIK-MIB::mtxrHlTemperature",
                                },
                                {
                                    "name": "hw_cpu_temp",
                                    "oid": "MIKROTIK-MIB::mtxrHlCpuTemperature",
                                },
                                {
                                    "name": "hw_board_temp",
                                    "oid": "MIKROTIK-MIB::mtxrHlBoardTemperature",
                                },
                                {
                                    "name": "hw_fan1_rpm",
                                    "oid": "MIKROTIK-MIB::mtxrHlFanSpeed1",
                                },
                                {
                                    "name": "hw_fan2_rpm",
                                    "oid": "MIKROTIK-MIB::mtxrHlFanSpeed2",
                                },
                            ],
                            "table": [
                                # MikroTik Health (table)
                                {
                                    "name": "hw",
                                    "oid": "MIKROTIK-MIB::mtxrGaugeTable",
                                    "field": [
                                        {
                                            "name": "sensor",
                                            "oid": "MIKROTIK-MIB::mtxrGaugeName",
                                            "is_tag": True,
                                        },
                                        {
                                            "name": "value",
                                            "oid": "MIKROTIK-MIB::mtxrGaugeValue",
                                        },
                                        {
                                            "name": "unit",
                                            "oid": "MIKROTIK-MIB::mtxrGaugeUnit",
                                            "is_tag": True,
                                        },
                                    ],
                                },
                                # Interface statistics
                                {
                                    "name": "interface",
                                    "oid": "IF-MIB::ifTable",
                                    "field": [
                                        # 6: ethernetCsmacd (physischer Ethernet-Port)
                                        # 24: softwareLoopback
                                        # 53: propVirtual (oft VLANs bei MikroTik)
                                        # 131: tunnel
                                        # 135: l2vlan
                                        # 161: ieee8023adLag (Bonding/LACP)
                                        # 209: bridge
                                        {
                                            "name": "ifType",
                                            "oid": "IF-MIB::ifType",
                                            "is_tag": True,
                                        },

                                        # Labels (optional but recommended)
                                        {
                                            "name": "ifName",
                                            "oid": "IF-MIB::ifName",
                                            "is_tag": True,
                                        },
                                        {
                                            "name": "ifAlias",
                                            "oid": "IF-MIB::ifAlias",
                                            "is_tag": True,
                                        },

                                        # Bytes (64-bit)
                                        {
                                            "name": "in_octets",
                                            "oid": "IF-MIB::ifHCInOctets",
                                        },
                                        {
                                            "name": "out_octets",
                                            "oid": "IF-MIB::ifHCOutOctets",
                                        },

                                        # Packets (64-bit unicast)
                                        {
                                            "name": "in_ucast_pkts",
                                            "oid": "IF-MIB::ifHCInUcastPkts",
                                        },
                                        {
                                            "name": "out_ucast_pkts",
                                            "oid": "IF-MIB::ifHCOutUcastPkts",
                                        },
                                        {
                                            "name": "in_mcast_pkts",
                                            "oid": "IF-MIB::ifHCInMulticastPkts",
                                        },
                                        {
                                            "name": "in_bcast_pkts",
                                            "oid": "IF-MIB::ifHCInBroadcastPkts",
                                        },
                                        {
                                            "name": "out_mcast_pkts",
                                            "oid": "IF-MIB::ifHCOutMulticastPkts",
                                        },
                                        {
                                            "name": "out_bcast_pkts",
                                            "oid": "IF-MIB::ifHCOutBroadcastPkts",
                                        },

                                        # Drops / Errors
                                        {
                                            "name": "in_discards",
                                            "oid": "IF-MIB::ifInDiscards",
                                        },
                                        {
                                            "name": "out_discards",
                                            "oid": "IF-MIB::ifOutDiscards",
                                        },
                                        {
                                            "name": "in_errors",
                                            "oid": "IF-MIB::ifInErrors",
                                        },
                                        {
                                            "name": "out_errors",
                                            "oid": "IF-MIB::ifOutErrors",
                                        },
                                    ],
                                },
                                # PoE
                                {
                                    "name": "poe",
                                    "oid": "MIKROTIK-MIB::mtxrPOETable",
                                    "field": [
                                        {
                                            "name": "ifName",
                                            "oid": "IF-MIB::ifName",
                                            "is_tag": True,
                                        },
                                        {
                                            "name": "ifAlias",
                                            "oid": "IF-MIB::ifAlias",
                                            "is_tag": True,
                                        },
                                        {
                                            "name": "ifindex",
                                            "oid": "MIKROTIK-MIB::mtxrPOEInterfaceIndex",
                                            "is_tag": True,
                                        },
                                        {
                                            "name": "status",
                                            "oid": "MIKROTIK-MIB::mtxrPOEStatus",
                                        },
                                        {
                                            "name": "voltage",
                                            "oid": "MIKROTIK-MIB::mtxrPOEVoltage",
                                        },
                                        {
                                            "name": "current",
                                            "oid": "MIKROTIK-MIB::mtxrPOECurrent",
                                        },
                                        {
                                            "name": "power",
                                            "oid": "MIKROTIK-MIB::mtxrPOEPower",
                                        },
                                    ],
                                },
                            ],
                        })
                            for routeros_node in repo.nodes_in_group("routeros")
                    },
                },
            },
        },
    }
