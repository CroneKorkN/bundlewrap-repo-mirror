from tomlkit import dumps

files['/etc/telegraf/telegraf.conf'] = {
    'content': dumps(node.metadata.get('telegraf/config'), sort_keys=True),
    'triggers': [
        'svc_systemd:telegraf:restart',
    ],
}

svc_systemd['telegraf'] = {
    'needs': [
        'file:/etc/telegraf/telegraf.conf',
        'pkg_apt:telegraf',
    ],
}
