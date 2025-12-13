from ipaddress import ip_address

def _values_from_all_nodes(type, name, zone):
    return {
        value
            for node in repo.nodes
            for value in node.metadata.get(f'dns/{name}{"." if name else ""}{zone}/{type}', [])
    }

def record_matches_view(value, type, name, zone, view, metadata):
    if type not in ['A', 'AAAA']:
        return True

    if metadata.get(f'bind/views/{view}/is_internal'):
        if ip_address(value).is_private:
            return True
        elif not list(filter(
            lambda other_value: ip_address(other_value).is_private,
            _values_from_all_nodes(type, name, zone),
        )):
            return True
    else:
        if ip_address(value).is_global:
            return True
        elif not list(filter(
            lambda other_value: ip_address(other_value).is_global,
            _values_from_all_nodes(type, name, zone),
        )):
            return True
