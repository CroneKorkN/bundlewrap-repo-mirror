files[node.metadata.get('hostname_file')] = {
    'content': node.metadata.get('hostname'),
    'triggers': [
        'action:update_hostname',
    ],
}

actions["update_hostname"] = {
    "command": f"hostname -F {node.metadata.get('hostname_file')}",
    'triggered': True,
}
