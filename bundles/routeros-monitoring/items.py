files = {
    # https://mikrotik.com/download/tools
    '/usr/share/snmp/mibs/MIKROTIK-MIB.txt': {
        'source': 'mikrotik.mib',
        'mode': '0644',
        'needed_by': {
            'svc_systemd:telegraf.service',
        },
    },
}
