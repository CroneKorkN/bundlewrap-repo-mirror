@metadata_reactor
def backup_authorized_keys(metadata):
    for other_node in repo.nodes:
        if other_node.metadata.get('backup/server') == node.name:
                other_node.metadata.get('users/root/pubkey')
        
    return {}
