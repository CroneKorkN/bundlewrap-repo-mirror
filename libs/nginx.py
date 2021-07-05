def render_config(config):
    return '\n'.join(render_lines(config))

def render_lines(config, indent=0):
    lines = []
    blocks = []
    
    for key, value in sorted(config.items()):
        if isinstance(value, dict):
            blocks.extend([
                '',
                key+' {',
                *render_lines(value, indent=4),
                '}',
            ])
        elif isinstance(value, list):
            lines.extend([
                f'{key} {_value};' for _value in value
            ])
        else:
            lines.append(
                f'{key} {value};'
            )
    
    return [
        f"{' '*indent}{line}" for line in lines+blocks
    ]
