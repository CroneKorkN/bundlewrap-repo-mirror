previous_action = []

for device, options in node.metadata.get('hdparm').items():
    for option, value in options.items():
        if option == 'power_management':
            name = f'hdparm_{option}_{device}'
            actions[name] = {
                'command': f'hdparm -B {value} "{device}"',
                'unless': f'hdparm -B "{device}" | grep APM_level | cut -d= -f2 | xargs | grep -q "^{value}$"',
                'needs': [
                    'pkg_apt:hdparm',
                    *previous_action,
                ],
            }
        else:
            raise ValueError(f'unsupported hdparm option: {option}')
            
    previous_action = [f'action:{name}']
