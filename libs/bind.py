from ipaddress import ip_address

def record_matches_view(value, type, name, zone, view, metadata, repo):
    if type not in ['A', 'AAAA']:
        return True

    if metadata.get(f'bind/views/{view}/is_internal'):        
        if ip_address(value).is_private:
            return True
        elif not list(filter(
            lambda other_value: ip_address(other_value).is_private,
            {
                other_value
                    for other_node in repo.nodes
                    if other_node.metadata.get(f'dns/{name}.{zone}/{type}', [])
                    for other_value in other_node.metadata.get(f'dns/{name}.{zone}/{type}')
            }
        )):
            return True
    else:
        if ip_address(value).is_global:
            return True
        elif not list(filter(
            lambda other_value: ip_address(other_value).is_global,
            {
                other_value
                    for other_node in repo.nodes
                    if other_node.metadata.get(f'dns/{name}.{zone}/{type}', [])
                    for other_value in other_node.metadata.get(f'dns/{name}.{zone}/{type}')
            }
        )):
            return True
