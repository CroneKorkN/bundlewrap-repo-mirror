files = {
    '/usr/local/share/telegraf/smartctl_power_mode': {
        'source': 'telegraf_plugin_power_mode',
        'content_type': 'mako',
        'mode': '0755',
    },
    '/usr/local/share/telegraf/smartctl_errors': {
        'source': 'telegraf_plugin_errors',
        'content_type': 'mako',
        'mode': '0755',
    },
}

previous_action = []

for device, conf in node.metadata.get('smartctl').items():
    for option, value in conf.items():
        if option == 'apm':
            action_name = f'smartctl_apm_{device}'
            actions[action_name] = {
                'command': f'smartctl --set apm,{value} "{device}"',
                'unless': f'smartctl --get apm "{device}" --json=c | jq .ata_apm.level | grep -q "^{value}$"',
                'needs': [
                    'pkg_apt:smartmontools',
                    *previous_action,
                ],
            }
        else:
            raise ValueError(f'{node.name}: unkown smartctl option: {option}')

        previous_action = [f'action:{action_name}']
