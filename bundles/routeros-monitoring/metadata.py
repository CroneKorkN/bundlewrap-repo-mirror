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
                "processors": {
                    "enum": [
                        h({
                            "tagpass": {
                                "operating_system": ["routeros"],
                            },
                            "mapping": [
                                h({
                                    "tag": "agent_host",
                                    "dest": "host",
                                    "default": "unknown",
                                    "value_mappings": {
                                        routeros_node.hostname: routeros_node.name
                                            for routeros_node in repo.nodes_in_group("routeros")
                                    },
                                })
                            ]
                        })
                    ]
                },
                "inputs": {
                    "snmp": {
                        h({
                            "agents": [
                                f"udp://{routeros_node.hostname}:161"
                                    for routeros_node in repo.nodes_in_group("routeros")
                            ],
                            "version": 2,
                            "community": "public",
                            "interval": "30s",
                            "tags": {
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
                                # Interface statistics (standard IF-MIB)
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
                                # Interface statistics (MikroTik-specific mib)
                                {
                                    "name": "interface_errors",
                                    "oid": "MIKROTIK-MIB::mtxrInterfaceStatsTable",
                                    "field": [
                                        # Join key / label (usually identical to IF-MIB ifName)
                                        {
                                            "name": "ifName",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsName",
                                            "is_tag": True,
                                        },

                                        # join IF-MIB for better labels
                                        {
                                            "name": "ifAlias",
                                            "oid": "IF-MIB::ifAlias",
                                            "is_tag": True,
                                        },

                                        # =========================
                                        # Physical layer (L1/L2)
                                        # =========================
                                        # CRC/FCS errors → very often cabling, connectors, SFPs, signal quality (EMI)
                                        {
                                            "name": "rx_fcs_errors",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsRxFCSError",
                                        },
                                        # Alignment errors → typically duplex mismatch or PHY problems
                                        {
                                            "name": "rx_align_errors",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsRxAlignError",
                                        },
                                        # Code errors → PHY encoding errors (signal/SFP/PHY)
                                        {
                                            "name": "rx_code_errors",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsRxCodeError",
                                        },
                                        # Carrier errors → carrier lost (copper issues, autoneg, PHY instability)
                                        {
                                            "name": "rx_carrier_errors",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsRxCarrierError",
                                        },
                                        # Jabber → extremely long invalid frames (faulty NIC/PHY, very severe)
                                        {
                                            "name": "rx_jabber",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsRxJabber",
                                        },

                                        # ==================================
                                        # Length / framing anomalies (diagnostic)
                                        # ==================================
                                        # Frames shorter than minimum (noise, collisions, broken sender)
                                        {
                                            "name": "rx_too_short",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsRxTooShort",
                                        },
                                        # Frames longer than allowed (MTU mismatch, framing errors)
                                        {
                                            "name": "rx_too_long",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsRxTooLong",
                                        },
                                        # Fragments (often collision-related or duplex mismatch)
                                        {
                                            "name": "rx_fragment",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsRxFragment",
                                        },
                                        # Generic length errors
                                        {
                                            "name": "rx_length_errors",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsRxLengthError",
                                        },

                                        # ==================
                                        # Drops (real packet loss)
                                        # ==================
                                        # RX drops (queue/ASIC/policy/overload) → highly alert-worthy
                                        {
                                            "name": "rx_drop",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsRxDrop",
                                        },
                                        # TX drops (buffer/queue exhaustion, scheduling, ASIC limits)
                                        {
                                            "name": "tx_drop",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsTxDrop",
                                        },

                                        # =========================================
                                        # Duplex / collision indicators
                                        # (should be zero on full-duplex links)
                                        # =========================================
                                        # Total collisions (relevant only for half-duplex or misconfigurations)
                                        {
                                            "name": "tx_collisions",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsTxCollision",
                                        },
                                        # Late collisions → almost always duplex mismatch / bad autoneg
                                        {
                                            "name": "tx_late_collisions",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsTxLateCollision",
                                        },
                                        # Aggregate collision counter (context)
                                        {
                                            "name": "tx_total_collisions",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsTxTotalCollision",
                                        },
                                        # Excessive collisions → persistent duplex problems
                                        {
                                            "name": "tx_excessive_collisions",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsTxExcessiveCollision",
                                        },

                                        # ==================
                                        # Flow control (diagnostic)
                                        # ==================
                                        # Pause frames received (peer throttling you)
                                        {
                                            "name": "rx_pause",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsRxPause",
                                        },
                                        # Pause frames sent (you throttling the peer)
                                        {
                                            "name": "tx_pause",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsTxPause",
                                        },
                                        # Pause frames actually honored
                                        {
                                            "name": "tx_pause_honored",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsTxPauseHonored",
                                        },

                                        # ==========
                                        # Stability
                                        # ==========
                                        # Link-down events (loose cables, bad SFPs, PoE power drops, reboots)
                                        {
                                            "name": "link_downs",
                                            "oid": "MIKROTIK-MIB::mtxrInterfaceStatsLinkDowns",
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
                    },
                },
            },
        },
    }
