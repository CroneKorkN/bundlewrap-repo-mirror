for network_name, network_conf in node.metadata.get('network').items():
    if 'qdisc' in network_conf:
        svc_systemd[f'qdisc-{network_name}.service'] = {
            'enabled': True,
            'running': None,
            'needs': {
                f'file:/usr/local/lib/systemd/system/qdisc-{network_name}.service',
            },
        }
        actions[f'qdisc-{network_name}.service_restart_workaround'] = {
            'command': 'true',
            'triggered': True,
            'triggered_by': {
                f'file:/usr/local/lib/systemd/system/qdisc-{network_name}.service',
            },
            'triggers': {
                f'svc_systemd:qdisc-{network_name}.service:restart',
            },
        }
