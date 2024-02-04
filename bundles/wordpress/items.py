files = {
    '/usr/lib/nagios/plugins/check_wordpress_insecure': {
        'mode': '0750',
    },
}

for site, conf in node.metadata.get('wordpress').items():
    directories[f'/opt/{site}'] = {
        'owner': 'www-data',
        'group': 'www-data',
        'mode': '0755',
    }
