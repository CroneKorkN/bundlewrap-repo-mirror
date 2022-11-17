waker_node = repo.get_node(node.metadata.get('wol-sleeper/waker'))
if not waker_node.has_bundle('wol-waker'):
    raise Exception(f'waker node {waker_node.name} does not have bundle wol-waker')

files = {
    '/usr/local/bin/suspend_if_idle': {
        'mode': '550',
    },
}

svc_systemd = {
    'wakeonlan-remove-downtime.service': {
        'enabled': True,
        'running': None,
    },
}
