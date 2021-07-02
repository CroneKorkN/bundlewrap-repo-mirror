assert node.has_bundle('redis')
assert node.has_bundle('postgresql')

from shlex import quote
import yaml


svc_systemd['grafana-server'] = {
    'needs': [
        'pkg_apt:grafana',
    ],
}

admin_password = node.metadata.get('grafana/config/security/admin_password')
port = node.metadata.get('grafana/config/server/http_port')
actions['reset_grafana_admin_password'] = {
    'command': f"grafana-cli admin reset-admin-password {quote(admin_password)}",
    'unless': f"curl http://admin:{quote(admin_password)}@localhost:{port}/api/org",
    'needs': [
        'svc_systemd:grafana-server',
    ],
}

directories = {
    '/etc/grafana': {
    },
    '/etc/grafana/provisioning': {
    },
    '/etc/grafana/provisioning/datasources': {
        'purge': True,
    },
}

files = {
    '/etc/grafana/grafana.ini': {
        'content': repo.libs.ini.dumps(node.metadata.get('grafana/config')),
        'triggers': [
            'svc_systemd:grafana-server:restart',
        ],
    },
    '/etc/grafana/provisioning/datasources/managed.yaml': {
        'content': yaml.dump({
            'apiVersion': 1,
            'datasources': list(node.metadata.get('grafana/datasources').values()),
        }),
        'triggers': [
            'svc_systemd:grafana-server:restart',
        ],
    },
}
