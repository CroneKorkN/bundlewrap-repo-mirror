svc_systemd['cron'] = {
    'enabled': node.metadata.get('systemd_timers/cron/enabled', False),
    'running': node.metadata.get('systemd_timers/cron/enabled', False),
}

files['/usr/lib/nagios/plugins/check_systemd_timer'] = {
    'mode': '0755',
}
