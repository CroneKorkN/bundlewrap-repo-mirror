for domain, conf in node.metadata.get('wordpress').items():
    directories = {
        f'/opt/wordpress/{domain}': {
            'owner': 'www-data',
            'group': 'www-data',
            'mode': '0755',
        },
    }
