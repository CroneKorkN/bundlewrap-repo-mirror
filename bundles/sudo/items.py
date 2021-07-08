directories = {
    '/etc/sudoers.d': {
        'purge': True,
    },
}

for user, commands in node.metadata.get('sudoers').items():
    files[f'/etc/sudoers.d/{user}'] = {
        'content': f"{user} ALL=(ALL) NOPASSWD: {', '.join(commands)}",
        'mode': '500',
    }
