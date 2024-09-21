from shlex import quote

def generate_sysctl_key_value_pairs_from_json(json_data, parents=[]):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            yield from generate_sysctl_key_value_pairs_from_json(value, [*parents, key])
    elif isinstance(json_data, list):
        raise ValueError(f"List not supported: '{json_data}'")
    else:
        # If it's a leaf node, yield the path
        yield (parents, json_data)

key_value_pairs = generate_sysctl_key_value_pairs_from_json(node.metadata.get('sysctl'))


files= {
    '/etc/sysctl.conf': {
        'content': '\n'.join(
            sorted(
                f"{'.'.join(path)}={value}"
                    for path, value in key_value_pairs
            ),
        ),
        'triggers': [
            'svc_systemd:systemd-sysctl.service:restart',
        ],
    },
}

svc_systemd = {
    'systemd-sysctl.service': {},
}

for path, value in key_value_pairs:
    actions[f'reload_sysctl.conf_{path}'] = {
        'command': f"sysctl --values {'.'.join(path)}  | grep -q {quote('^'+value+'$')}",
        'needs': [
            f'action:systemd-sysctl.service',
            f'action:systemd-sysctl.service:restart',
        ],
    }
