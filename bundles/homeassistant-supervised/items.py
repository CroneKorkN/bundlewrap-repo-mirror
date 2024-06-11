from shlex import quote


version = node.metadata.get('homeassistant/os_agent_version')

directories = {
    '/usr/share/hassio': {},
}

actions = {
    'install_os_agent': {
        'command': ' && '.join([
            f'wget -O /tmp/os-agent.deb https://github.com/home-assistant/os-agent/releases/download/{quote(version)}/os-agent_{quote(version)}_linux_aarch64.deb',
            'DEBIAN_FRONTEND=noninteractive dpkg -i /tmp/os-agent.deb',
        ]),
        'unless': f'test "$(apt -qq list os-agent | cut -d" " -f2)" = "{quote(version)}"',
        'needs': {
            'pkg_apt:',
            'zfs_dataset:tank/homeassistant',
        },
    },
    'install_homeassistant_supervised': {
        'command': 'wget -O /tmp/homeassistant-supervised.deb https://github.com/home-assistant/supervised-installer/releases/latest/download/homeassistant-supervised.deb && apt install /tmp/homeassistant-supervised.deb',
        'unless': 'apt -qq list homeassistant-supervised | grep -q "installed"',
        'needs': {
            'action:install_os_agent',
        },
    },
}

