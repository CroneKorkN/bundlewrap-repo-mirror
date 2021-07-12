files['/etc/hostname'] = {
    'content': node.metadata.get('hostname'),
    'triggers': [
        'action:update_hostname',
    ],
}

actions["update_hostname"] = {
    "command": "hostname -F /etc/hostname",
    'triggered': True,
}
