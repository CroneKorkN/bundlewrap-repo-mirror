"""backup: names shared by the backup client and server bundles."""


def user_for(client_node):
    """The user a backup client logs in as on its backup server.

    From its id rather than its name, so renaming a node leaves the server untouched;
    the first 8 characters, as user names may not exceed 32.
    """
    return 'backup-' + client_node.metadata.get('id')[:8]
