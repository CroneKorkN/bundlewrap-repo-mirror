locale = node.metadata.get('locale')

files = {
    '/etc/locale.gen': {
        'content': f"{locale} {locale.split('.')[1]}\n",
        'triggers': {
            'action:locale-gen',
        },
    }
}

actions = {
    'locale-gen': {
        'command': 'locale-gen',
        'triggered': True,
    },
    'systemd-locale': {
        'command': f'localectl set-locale LANG="{locale}"',
        'unless': f'localectl | grep -Fi "system locale" | grep -Fi "{locale}"',
        'preceded_by': {
            'action:locale-gen',
        },
        'needs': {
            'action:locale-gen',
        },
    },
}
