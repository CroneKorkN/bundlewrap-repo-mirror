files = {
    '/opt/tasmota-charge': {
        'owner': 'tasmota-charge',
        'mode': '0550',
        'content_type': 'mako',
        'context': {
            'phone_ip': node.metadata.get('tasmota-charge/phone/ip'),
            'phone_user': node.metadata.get('tasmota-charge/phone/user'),
            'plug_ip': node.metadata.get('tasmota-charge/plug/ip'),
            'min': node.metadata.get('tasmota-charge/plug/min'),
            'max': node.metadata.get('tasmota-charge/plug/max'),
        }
    },
}
