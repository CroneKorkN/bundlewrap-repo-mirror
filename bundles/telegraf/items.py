from tomlkit import dumps

files['/etc/telegraf/telegraf.conf'] = {
    'content': dumps(node.metadata.get('telegraf/config')),
    'triggers': [
        'svc_systemd:telegraf:restart',
    ],
}

svc_systemd['telegraf'] = {
    'needs': [
        'file:/etc/telegraf/telegraf.conf',
    ],
}
