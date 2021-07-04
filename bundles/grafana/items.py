assert node.has_bundle('redis')
assert node.has_bundle('postgresql')

from mako.template import Template
from shlex import quote
from copy import deepcopy
import yaml
import json
from itertools import count

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

monitored_nodes = [
    other_node
        for other_node in repo.nodes
        if other_node.metadata.get('telegraf/influxdb_node', None) == node.metadata.get('grafana/influxdb_node')
]

for dashboard_id, monitored_node in enumerate(monitored_nodes, start=1):
    dashboard = deepcopy(dashboard_template)
    dashboard['id'] = dashboard_id
    dashboard['title'] = monitored_node.name
    panel_id = count(start=1)

    
    for row_id, row_name in enumerate(sorted(monitored_node.metadata.get('grafana_rows')), start=1):
        with open(repo.path.join([f'data/grafana/rows/{row_name}.py'])) as file:
            row = eval(file.read())
        
        for panel_in_row, (panel_name, panel_config) in enumerate(row.items()):
            panel = deepcopy(panel_template)
            panel['id'] = next(panel_id)
            panel['title'] = panel_name
            panel['gridPos']['w'] = 24 // len(row)
            panel['gridPos']['x'] = (24 // len(row)) * panel_in_row
            panel['gridPos']['y'] = (row_id - 1) * panel['gridPos']['h']
            
            if 'display_name' in panel_config:
                panel['fieldConfig']['defaults']['displayName'] = '${'+panel_config['display_name']+'}'

            if panel_config.get('stacked', False):
                panel['fieldConfig']['defaults']['custom']['stacking']['mode'] = 'normal'
            else:
                panel['fieldConfig']['defaults']['custom']['stacking']['mode'] = 'none'
            
            for query_name, query_config in panel_config['queries'].items():
                panel['targets'].append({
                    'refId': query_name,
                    'query': flux_template.render(
                        bucket=bucket,
                        host=monitored_node.name,
                        filters={
                            'host': monitored_node.name,
                            **query_config['filters'],
                        },
                        function=query_config.get('function', None),
                    ).strip()
                })
                
            dashboard['panels'].append(panel)
    
    files[f'/var/lib/grafana/dashboards/{monitored_node.name}.json'] = {
        'content': json.dumps(dashboard, sort_keys=True, indent=4),
        'triggers': [
            'svc_systemd:grafana-server:restart',
        ]
    }
        
