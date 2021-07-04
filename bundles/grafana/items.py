assert node.has_bundle('redis')
assert node.has_bundle('postgresql')

from mako.template import Template
from shlex import quote
from copy import deepcopy
import yaml
import json

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
    '/etc/grafana/provisioning/dashboards': {
        'purge': True,
    },
    '/var/lib/grafana': {},
    '/var/lib/grafana/dashboards': {},
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
    '/etc/grafana/provisioning/dashboards/managed.yaml': {
        'content': yaml.dump({
            'apiVersion': 1,
            'providers': [{
                'name': 'Default',
                'folder': 'Generated',
                'type': 'file',
                'options': {
                    'path': '/var/lib/grafana/dashboards',
                },
            }],
        }),
        'triggers': [
            'svc_systemd:grafana-server:restart',
        ],
    },
}

# DASHBOARDS

with open(repo.path.join([f'data/grafana/dashboard.py'])) as file:
    dashboard_template = eval(file.read())
with open(repo.path.join([f'data/grafana/panel.py'])) as file:
    panel_template = eval(file.read())
with open(repo.path.join([f'data/grafana/flux.mako'])) as file:
    flux_template = Template(file.read())

bucket = repo.get_node(node.metadata.get('grafana/influxdb_node')).metadata.get('influxdb/bucket')

for dashboard_id, (node_name, panels) in enumerate(node.metadata.get('grafana/dashboards').items(), start=1):
    dashboard = deepcopy(dashboard_template)
    dashboard['id'] = dashboard_id
    dashboard['title'] = node_name
    
    for panel_id, (panel_name, panel_config) in enumerate(panels.items(), start=1):
        panel = deepcopy(panel_template)
        panel['id'] = panel_id
        panel['title'] = panel_name
        
        for target_name, target_config in panel_config.items():
            print(target_name, target_config)
            panel['targets'].append({
                'refId': target_name,
                'query': flux_template.render(
                    bucket=bucket,
                    host=node_name,
                    field=target_name,
                    filters=target_config['filter'],
                ).strip()
            })
            
        dashboard['panels'].append(panel)
    
    files[f'/var/lib/grafana/dashboards/{node_name}.json'] = {
        'content': json.dumps(dashboard, sort_keys=True, indent=4),
        'triggers': [
            'svc_systemd:grafana-server:restart',
        ]
    }
        
