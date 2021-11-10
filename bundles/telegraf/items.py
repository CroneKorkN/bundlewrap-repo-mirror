from tomlkit import dumps
import json
from bundlewrap.metadata import MetadataJSONEncoder


files['/etc/telegraf/telegraf.conf'] = {
    'content': dumps(json.loads(json.dumps(node.metadata.get('telegraf/config'), cls=MetadataJSONEncoder)), sort_keys=True),
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
