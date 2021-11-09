default_locale = node.metadata.get('locale/default')[0]

installed_locales = sorted([
    node.metadata.get('locale/default'),
    *node.metadata.get('locale/installed'),
])

files = {
    '/etc/locale.gen': {
        'content': '\n'.join(
            f'{locale} {type}' for locale, type in installed_locales
        ),
        'triggers': {
            'action:locale-gen',
        },
    }
}

actions = {
    'locale-gen': {
        'command': 'locale-gen',
        'triggered': True,
        'needs': {
            'pkg_apt:locales',
        },
    },
    'systemd-locale': {
        'command': f'localectl set-locale LANG="{default_locale}"',
        'unless': f'localectl | grep -Fi "system locale" | grep -Fi "{default_locale}"',
        'preceded_by': {
            'action:locale-gen',
        },
    },
}
