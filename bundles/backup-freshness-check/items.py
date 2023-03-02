from json import dumps
from bundlewrap.metadata import MetadataJSONEncoder


files = {
    '/etc/backup-freshness-check.json': {
        'content': dumps({
            'prefix': node.metadata.get('backup-freshness-check/prefix'),
            'datasets': node.metadata.get('backup-freshness-check/datasets'),
        }, indent=4, sort_keys=True, cls=MetadataJSONEncoder),
    },
    '/usr/lib/nagios/plugins/check_backup_freshness': {
        'mode': '0755',
    },
}
