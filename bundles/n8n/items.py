assert node.has_bundle('nodejs')
assert node.has_bundle('postgresql')
assert node.has_bundle('zfs')

# To update:
#
# - systemctl stop n8n postgresql
# - tempsnap pre-n8n-update            (for psql, emergency rollback)
# - apply

version = node.metadata.get("n8n/version")
actions['install_n8n'] = {
    'command': f'cd /opt/n8n && sudo -u n8n npm install n8n@{version}',
    'unless': f'test -e /opt/n8n/node_modules && '
              f'test $(jq -r ".version" < /opt/n8n/node_modules/n8n/package.json) = "{version}"',
    'needs': {
        'directory:/opt/n8n',
        'pkg_apt:nodejs',
        'user:n8n',
    },
    'triggers': {
        'svc_systemd:n8n.service:restart',
    },
}

svc_systemd['n8n.service'] = {
    'enabled': True,
    'running': True,
    'needs': {
        'pkg_apt:nodejs',
        'action:install_n8n',
    },
}
