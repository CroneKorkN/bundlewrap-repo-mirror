"""backup: names shared by the backup client and server bundles."""


def user_for(client_node):
    """The user a backup client logs in as on its backup server."""
    return 'backup-' + client_node.name.replace('.', '-')
