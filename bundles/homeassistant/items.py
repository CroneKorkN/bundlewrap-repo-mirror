users = {
    'homeassistant': {
        'home': '/opt/homeassistant',
        'groups': [
            'dialout',
            #'gpio',
            #'i2c',
        ],
    },
}

directories = {
    '/opt/homeassistant': {
        'owner': 'homeassistant',
        'group': 'homeassistant',
    },
    '/opt/homeassistant/data': {
        'owner': 'homeassistant',
        'group': 'homeassistant',
    },
    '/opt/homeassistant/venv': {
        'owner': 'homeassistant',
        'group': 'homeassistant',
    },
}

svc_systemd = {
    'homeassistant.service': {},
}

# venv manually managed for now
'''
python3 -m venv /opt/homeassistant/venv
source /opt/homeassistant/venv/bin/activate
python3 -m pip install wheel
pip3 install homeassistant
'''
