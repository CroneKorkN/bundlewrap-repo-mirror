import tomlkit
import json
from bundlewrap.metadata import MetadataJSONEncoder

files = {
    '/etc/telegraf/telegraf.conf': {
        'content': tomlkit.dumps(
            json.loads(json.dumps(
                node.metadata.get('telegraf/config'),
                cls=MetadataJSONEncoder,
            )),
            sort_keys=True,
        ),
        'triggers': [
            'svc_systemd:telegraf.service:restart',
        ],
    },
    '/usr/local/share/telegraf/procio': {
        'content_type': 'download',
        'source': f"https://dl.sublimity.de/telegraf-procio/telegraf-procio-{node.metadata.get('system/architecture')}-latest",
        'mode': '0755',
    },
    '/usr/local/share/telegraf/pressure_stall': {
        'content_type': 'download',
        'source': f"https://dl.sublimity.de/telegraf-pressure-stall/telegraf-pressure-stall-{node.metadata.get('system/architecture')}-latest",
        'mode': '0755',
    },
}

svc_systemd['telegraf.service'] = {
    'needs': [
        'file:/etc/telegraf/telegraf.conf',
        'pkg_apt:telegraf',
    ],
}
