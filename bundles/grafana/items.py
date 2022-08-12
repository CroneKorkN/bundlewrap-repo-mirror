assert node.has_bundle('redis')
assert node.has_bundle('postgresql')

from mako.template import Template
from shlex import quote
from copy import deepcopy
from itertools import count
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
    '/var/lib/grafana/dashboards': {
        'purge': True,
        'triggers': [
            'svc_systemd:grafana-server:restart',
        ],
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
    dashboard['uid'] = monitored_node.metadata.get('id')
    panel_id = count(start=1)

    for row_id, row_name in enumerate(sorted(monitored_node.metadata.get('grafana_rows')), start=1):
        with open(repo.path.join([f'data/grafana/rows/{row_name}.py'])) as file:
            row = eval(file.read())

        for panel_in_row, (panel_name, panel_config) in enumerate(row.items()):
            panel = deepcopy(panel_template)
            panel['id'] = next(panel_id)
            panel['title'] = f'{row_name} {panel_name}'
            panel['gridPos']['w'] = 24 // len(row)
            panel['gridPos']['x'] = (24 // len(row)) * panel_in_row
            panel['gridPos']['y'] = (row_id - 1) * panel['gridPos']['h']

            if 'display_name' in panel_config:
                panel['fieldConfig']['defaults']['displayName'] = '${'+panel_config['display_name']+'}'

            if panel_config.get('stacked'):
                panel['fieldConfig']['defaults']['custom']['stacking']['mode'] = 'normal'

            if 'unit' in panel_config:
                panel['fieldConfig']['defaults']['unit'] = panel_config['unit']

            if 'min' in panel_config:
                panel['fieldConfig']['defaults']['min'] = panel_config['min']
            if 'max' in panel_config:
                panel['fieldConfig']['defaults']['max'] = panel_config['max']
            if 'soft_max' in panel_config:
                panel['fieldConfig']['defaults']['custom']['axisSoftMax'] = panel_config['soft_max']

            if 'legend' in panel_config:
                panel['options']['legend'].update(panel_config['legend'])

            if 'tooltip' in panel_config:
                panel['options']['tooltip']['mode'] = panel_config['tooltip']
                if panel_config['tooltip'] == 'multi':
                    panel['options']['tooltip']['sort'] = 'desc'

            for query_name, query_config in panel_config['queries'].items():
                panel['targets'].append({
                    'refId': query_name,
                    'query': flux_template.render(
                        bucket=bucket,
                        host=monitored_node.name,
                        negative=query_config.get('negative', False),
                        boolean_to_int=query_config.get('boolean_to_int', False),
                        minimum=query_config.get('minimum', None),
                        filters={
                            'host': monitored_node.name,
                            **query_config['filters'],
                        },
                        function=query_config.get('function', None),
                    ).strip()
                })

            dashboard['panels'].append(panel)

    files[f'/var/lib/grafana/dashboards/{monitored_node.name}.json'] = {
        'content': json.dumps(dashboard, indent=4),
        'triggers': [
            'svc_systemd:grafana-server:restart',
        ]
    }

