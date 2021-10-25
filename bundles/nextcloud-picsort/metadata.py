from shlex import quote as q


@metadata_reactor.provides(
    'systemd-timers',
)
def systemd_timers(metadata):
    return {
        'systemd-timers': {
            f'nextcloud-picsort-{user}': {
                'command': f'/opt/nextcloud-picsort {q(user)} {q(paths["source"])} {q(paths["destination"])}',
                'when': '*:0/10',
            }
                for user, paths in metadata.get('nextcloud-picsort').items()
        }
    }
