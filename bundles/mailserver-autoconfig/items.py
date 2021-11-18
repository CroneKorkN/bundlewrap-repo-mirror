autoconfig_hostname = node.metadata.get('mailserver/autoconfig_hostname')

files = {
    f'/var/www/{autoconfig_hostname}/mail/config-v1.1.xml': {
        'content_type': 'mako',
        'context': {
            'mailserver': node.metadata.get('mailserver/hostname'),
            'autoconfig': autoconfig_hostname,
        },
        'owner': 'www-data',
    },
    f'/var/www/{autoconfig_hostname}/autodiscover/autodiscover.php': {
        'content_type': 'mako',
        'owner': 'www-data',
    },
}
