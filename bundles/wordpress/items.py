for site, conf in node.metadata.get('wordpress').items():
    directories = {
        f'/opt/wordpress/{site}': {
            'owner': 'www-data',
            'group': 'www-data',
            'mode': '0755',
        },
    }
