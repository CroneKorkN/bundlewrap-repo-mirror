defaults = {
    'users': {
        'tasmota-charge': {
            'home': '/home/tasmota-charge',
        },
    },
    'systemd-timers': {
        'tasmota-charge': {
            'command': f'/usr/bin/sudo -u tasmota-charge /opt/tasmota-charge',
            'when': 'minutely',
        },
    }
}
