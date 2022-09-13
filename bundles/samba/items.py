from shlex import quote

files = {
    '/etc/samba/smb.conf': {
        'content_type': 'mako',
        'context': {
            'shares': {
                name: {
                    'comment': name,
                    'path': f'/var/lib/samba/usershares/{name}',
                    'valid users': name,
                    'public': 'no',
                    'writable': 'yes',
                    'browsable': 'yes',
                }
                    for name, conf in node.metadata.get('samba/shares').items()
            },
        },
        'needs': [
            'pkg_apt:samba',
        ],
        'triggers': [
            'svc_systemd:smbd.service:restart',
        ],
    },
}

directories = {
    '/var/lib/samba/usershares': {
        'mode': '1751',
    },
}


svc_systemd = {
    'smbd.service': {},
}

for name, conf in node.metadata.get('samba/shares').items():
    quoted_password = quote(str(conf['password']))
    actions[f'samba_password_{name}'] = {
        'command': f"(echo {quoted_password}; echo {quoted_password}) | smbpasswd -s -a {name}",
        'unless': f"echo {quoted_password} | smbclient -U {name} //localhost/{name} -c 'ls'",
        'needs': [
            f'user:{name}',
            'svc_systemd:smbd.service:restart',
        ],
    }

    directories[f'/var/lib/samba/usershares/{name}'] = {
        'owner': name,
        'group': name,
        'needs': [
            f'zfs_dataset:tank/samba/{name}',
        ],
    }


# TTMx36kcLbdkdgOqvxjlX03tLCjgeyXq
