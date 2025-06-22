from json import dumps
from bundlewrap.metadata import MetadataJSONEncoder

files = {
    '/etc/kea/kea-dhcp4.conf': {
        'content': dumps(node.metadata.get('kea'), indent=4, sort_keys=True, cls=MetadataJSONEncoder),
        'triggers': [
            'svc_systemd:kea-dhcp4-server:restart',
        ],
    },
}

svc_systemd = {
    'kea-dhcp4-server': {
        'needs': [
            'pkg_apt:kea-dhcp4-server',
            'file:/etc/kea/kea-dhcp4.conf',
            'svc_systemd:systemd-networkd.service:restart',
        ],
    },
}
