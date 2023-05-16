from shlex import quote as q


defaults = {
    'apt': {
        'packages': {
            'libimage-exiftool-perl': {},
        },
    },
}


@metadata_reactor.provides(
    'systemd-timers',
)
def systemd_timers(metadata):
    return {
        'systemd-timers': {
            f'nextcloud-picsort-{user}': {
                'command': f'/opt/nextcloud-picsort',
                'when': '*:0/30',
                'env': {
                    'USER': user,
                    'SOURCE_DIR': paths["source"],
                    'DESTINATION_DIR': paths["destination"],
                    'UNSORTABLE_DIR': paths["unsortable"],
                },
            }
                for user, paths in metadata.get('nextcloud-picsort').items()
        }
    }
