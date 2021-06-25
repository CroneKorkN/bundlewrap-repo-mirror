defaults = {
    'users': {
        'backup-receiver': {
            'authorized_keys': [],
        },
    },
}


@metadata_reactor.provides(
    'users/backup-receiver/authorized_keys'
)
def backup_authorized_keys():
    return
