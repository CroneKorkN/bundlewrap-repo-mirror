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
                'check_interval': '6h',
                'vars.sudo': True,
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
