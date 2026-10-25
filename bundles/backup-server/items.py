from json import dumps


directories['/opt/backup-server'] = {}

files['/opt/backup-server/prune-snapshots'] = {
    'mode': '755',
}

files['/opt/backup-server/prune-all-snapshots'] = {
    'mode': '755',
}

# replaced by one user per client, see below
files['/etc/sudoers.d/backup-receiver'] = {
    'delete': True,
}
files['/home/backup-receiver/.ssh/authorized_keys'] = {
    'delete': True,
}

for other_node in repo.nodes:
    if (
        other_node.dummy
        or not other_node.has_bundle('backup')
        or other_node.metadata.get('backup/server') != node.name
    ):
        continue

    user = repo.libs.backup.user_for(other_node)
    base_dataset = f"tank/{other_node.metadata.get('id')}"

    # no destroy: a compromised client cannot remove snapshots, not even its own;
    # rollback lets the initial recv -F replace the empty dataset created by bundlewrap
    permissions = 'create,mount,receive,rollback'
    actions[f'zfs_allow_{user}'] = {
        'command': f'zfs allow -u {user} {permissions} {base_dataset}',
        'unless': f"zfs allow {base_dataset} | grep -qx '[[:space:]]*user {user} {permissions}'",
        'needs': [
            f'user:{user}',
            f'zfs_dataset:{base_dataset}',
        ],
    }

    # rsync runs as the client's user with --fake-super, ownership is kept in xattrs
    directories[f"/mnt/backups/{other_node.metadata.get('id')}"] = {
        'owner': user,
        'group': user,
        'mode': '0700',
        'needs': [
            f'zfs_dataset:{base_dataset}/fs',
        ],
        'triggers': [
            f'action:chown_backups_{user}',
        ],
    }
    actions[f'chown_backups_{user}'] = {
        'command': f"chown -R {user}: /mnt/backups/{other_node.metadata.get('id')}",
        'triggered': True,
    }

directories['/etc/backup-server'] = {}

files['/etc/backup-server/retention.json'] = {
    'content': dumps(node.metadata.get('backup-server/retention'), indent=4, sort_keys=True),
}
