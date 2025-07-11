# nano /etc/selinux/config
# SELINUX=disabled
# reboot

directories = {
    '/opt/bootshorn': {
        'owner': 'ckn',
        'group': 'ckn',
    },
    '/opt/bootshorn/recordings': {
        'owner': 'ckn',
        'group': 'ckn',
    },
    '/opt/bootshorn/recordings': {
        'owner': 'ckn',
        'group': 'ckn',
    },
    '/opt/bootshorn/recordings/processed': {
        'owner': 'ckn',
        'group': 'ckn',
    },
    '/opt/bootshorn/events': {
        'owner': 'ckn',
        'group': 'ckn',
    },
}

files = {
    '/opt/bootshorn/record': {
        'owner': 'ckn',
        'group': 'ckn',
        'mode': '755',
    },
    '/opt/bootshorn/process': {
        'owner': 'ckn',
        'group': 'ckn',
        'mode': '755',
    },
}

svc_systemd = {
    'bootshorn-record.service': {
        'needs': {
            'file:/opt/bootshorn/record',
        },
    },
}
