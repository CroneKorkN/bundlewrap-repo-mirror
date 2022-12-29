for package, conf in node.metadata.get('npm').items():
    actions[f'npm_{package}'] = {
        'command': f'npm install -g {package}',
        'unless': f"npm list -g -json | jq -r '.dependencies | keys[]' | grep -q '^{package}$'",
        'needs': [
            'pkg_apt:nodejs',
        ],
    }
