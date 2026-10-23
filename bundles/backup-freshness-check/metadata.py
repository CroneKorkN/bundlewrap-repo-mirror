defaults = {
    'backup-freshness-check': {
        'server': node.name,
        'prefix': 'auto-backup_',
        'datasets': {},
    },
    'monitoring': {
        'services': {
            'backup freshness': {
                'vars.command': '/usr/lib/nagios/plugins/check_backup_freshness',
                'check_interval': '24h',
                # a failed check would otherwise retry, and wake the server, every 30s
                'retry_interval': '6h',
                # the wakeup alone may take up to 10 minutes
                'check_timeout': 900,
                'vars.sudo': True,
            },
        },
    },
}


@metadata_reactor.provides(
    'monitoring/services/backup freshness/vars.wake',
)
def wake(metadata):
    if not node.has_bundle('wol-sleeper'):
        return {}

    return {
        'monitoring': {
            'services': {
                'backup freshness': {
                    'vars.wake': metadata.get('wol-sleeper/wake_command'),
                },
            },
        },
    }


@metadata_reactor.provides(
    'backup-freshness-check/datasets'
)
def backup_freshness_check(metadata):
    return {
        'backup-freshness-check': {
            'datasets': {
                f"{other_node.metadata.get('id')}/{dataset}"
                    for other_node in repo.nodes
                    if not other_node.dummy
                    and other_node.has_bundle('backup')
                    and other_node.has_bundle('zfs')
                    and other_node.metadata.get('backup/server') == metadata.get('backup-freshness-check/server')
                    for dataset, options in other_node.metadata.get('zfs/datasets').items()
                    if options.get('backup', True)
                    and not options.get('mountpoint', None) in [None, 'none']
            },
        },
    }
