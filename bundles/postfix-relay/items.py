from re import escape

# the mail server's own postfix delivers itself, see bundle postfix
if not node.has_bundle('postfix'):
    root = node.metadata.get('mail/root')

    file_options = {
        'content_type': 'mako',
        'needs': [
            'pkg_apt:postfix',
        ],
        'triggers': [
            'svc_systemd:postfix:restart',
        ],
    }

    files = {
        '/etc/postfix/main.cf': {
            'context': {
                'hostname': node.name,
                'relayhost': node.metadata.get('postfix-relay/relayhost'),
            },
            **file_options,
        },
        # every local recipient, root above all
        '/etc/postfix/virtual_alias': {
            'context': {
                'hostname': escape(node.name),
                'root': root,
            },
            **file_options,
        },
        # a sender in a domain of the mail server, which signs it
        '/etc/postfix/sender_canonical': {
            'context': {
                'hostname': escape(node.name),
                'sender': f"{node.name}@{root.split('@')[1]}",
            },
            **file_options,
        },
    }

    svc_systemd['postfix'] = {
        'needs': [
            'pkg_apt:postfix',
        ],
    }
