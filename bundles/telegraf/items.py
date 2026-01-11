import tomlkit


def inner_dict_to_list(dict_of_dicts):
    """
    Example:
    {
        'cpu': {
            'default': {'something': True},
            'another': {'something': False},
        },
    }
    becomes
    {
        'cpu': [
            {'something': True},
            {'something': False},
        ],
    }
    """
    return {
        key: [value for _, value in sorted(dicts.items())]
            for key, dicts in sorted(dict_of_dicts.items())
    }


files = {
    "/etc/telegraf/telegraf.conf": {
        'owner': 'telegraf',
        'group': 'telegraf',
        'mode': '0440',
        'needs': [
            "pkg_apt:telegraf",
        ],
        'content': tomlkit.dumps({
            'agent': node.metadata.get('telegraf/agent'),
            'inputs': inner_dict_to_list(node.metadata.get('telegraf/inputs')),
            'processors': inner_dict_to_list(node.metadata.get('telegraf/processors')),
            'outputs': inner_dict_to_list(node.metadata.get('telegraf/outputs')),
        }),
        'triggers': {
            'svc_systemd:telegraf.service:restart',
        },
    },
    '/usr/local/share/telegraf/procio': {
        'content_type': 'download',
        'source': f"https://dl.sublimity.de/telegraf-procio/telegraf-procio-{node.metadata.get('system/architecture')}-latest",
        'mode': '0755',
    },
    '/usr/local/share/telegraf/pressure_stall': {
        'content_type': 'download',
        'source': f"https://dl.sublimity.de/telegraf-pressure-stall/telegraf-pressure-stall-{node.metadata.get('system/architecture')}-latest",
        'mode': '0755',
    },
}

actions = {
    'telegraf-test-config': {
        'command': "sudo -u telegraf bash -c 'telegraf config check --config /etc/telegraf/telegraf.conf --strict-env-handling'",
        'triggered': True,
        'needs': [
            'bundle:sudo',
            'file:/etc/telegraf/telegraf.conf',
            'pkg_apt:telegraf',
        ],
    },
}

svc_systemd = {
    'telegraf.service': {
        'needs': ['pkg_apt:telegraf'],
        'preceded_by': {
            'action:telegraf-test-config',
        },
        'needs': {
            'action:telegraf-test-config',
        },
    },
}
