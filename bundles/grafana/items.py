assert node.has_bundle('redis')
assert node.has_bundle('postgresql')

from shlex import quote


files['/etc/grafana/grafana.ini'] = {
    'content': repo.libs.ini.dumps(node.metadata.get('grafana/config')),
    'triggers': [
        'svc_systemd:grafana-server:restart',
    ]
}

svc_systemd['grafana-server'] = {
    'needs': [
        'pkg_apt:grafana',
    ],
}

actions['reset_grafana_admin_password'] = {
    'command': f"grafana-cli admin reset-admin-password {quote(node.metadata.get('grafana/config/security/admin_password'))}",
    'needs': [
        'svc_systemd:grafana-server',
    ],
}
