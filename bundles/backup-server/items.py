from json import dumps
from bundlewrap.metadata import MetadataJSONEncoder


files = {
    '/etc/backup-server.json': {
        'content': dumps(node.metadata.get('backup-receiver'), indent=4, sort_keys=True, cls=MetadataJSONEncoder),
    },
    '/usr/lib/nagios/plugins/check_backup_freshness': {
        'mode': '0755',
    },
}
