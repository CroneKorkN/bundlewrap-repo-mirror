assert node.has_bundle('nginx')
assert node.has_bundle('php')
assert node.has_bundle('postgresql')


for domain, conf in node.metadata.get('wordpress').items():
    directories[conf['root']] = {
        'owner': 'www-data',
    }
