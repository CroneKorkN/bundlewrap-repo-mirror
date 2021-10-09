connections = {}

def get_connection(node, other_node):
    global connections
    
    node_id, other_node_id = node.metadata.get('id'), other_node.metadata.get('id')
    sorted_ids = tuple(sorted([node_id, other_node_id]))
    
    if sorted_ids not in connections:
        connections[sorted_ids] = {
            'pubkey': node.repo.libs.keys.get_pubkey_from_privkey(f'{other_node_id} wireguard pubkey', other_node.metadata.get('wireguard/privatekey')),
            'psk': node.repo.vault.random_bytes_as_base64_for(f"{sorted_ids[0]} wireguard {sorted_ids[1]}"),
        }

    return connections[sorted_ids]
