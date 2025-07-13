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
    '/opt/bootshorn/temperatures': {
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
    '/opt/bootshorn/temperature': {
        'content_type': 'mako',
        'context': {
            'hue_app_key': repo.vault.decrypt('encrypt$gAAAAABoc2WxZCLbxl-Z4IrSC97CdOeFgBplr9Fp5ujpd0WCCCPNBUY_WquHN86z8hKLq5Y04dwq8TdJW0PMSOSgTFbGgdp_P1q0jOBLEKaW9IIT1YM88h-JYwLf9QGDV_5oEfvnBCtO'),
        },
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
