svc_systemd['cron'] = {
    'enabled': False,
    'running': False,
}

files['/usr/lib/nagios/plugins/check_systemd_timer'] = {
    'mode': '0755',
}
