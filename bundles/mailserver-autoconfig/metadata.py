defaults = {}


@metadata_reactor.provides(
    'mailserver/autoconfig_hostname',
)
def hostname(metadata):
    return {
        'mailserver': {
            'autoconfig_hostname': f"autoconfig.{metadata.get('mailserver/hostname')}",
        },
    }


@metadata_reactor.provides(
    'nginx/vhosts',
)
def nginx(metadata):
    return {
        'nginx': {
            'vhosts': {
                metadata.get('mailserver/autoconfig_hostname'): {
                    'content': 'mailserver-autodiscover/vhost.conf',
                    'context': {
                        'root': f"/var/www/{metadata.get('mailserver/autoconfig_hostname')}",
                    },
                },
            },
        },
    }


@metadata_reactor.provides(
    'letsencrypt/domains',
)
def letsencrypt(metadata):
    return {
        'letsencrypt': {
            'domains': {
                metadata.get('mailserver/autoconfig_hostname'): {
                    'aliases': {
                        *{
                            f'autoconfig.{domain}'
                                for domain in metadata.get('mailserver/domains')
                        },
                        *{
                            f'autodiscover.{domain}'
                                for domain in metadata.get('mailserver/domains')
                        },
                    },
                },
            },
        },
    }


@metadata_reactor.provides(
    'dns',
)
def autoconfig(metadata):
    dns = {}
    
    for domain in metadata.get('mailserver/domains'):
        dns.update({
            f'autoconfig.{domain}': {
                'CNAME': {f"{metadata.get('mailserver/autoconfig_hostname')}."},
            },
            f'_autodiscover._tcp.{domain}': {
                'SRV': {f"10 10 443 {metadata.get('mailserver/autoconfig_hostname')}."},
            },
            f'autodiscover.{domain}': {
                'CNAME': {f"{metadata.get('mailserver/autoconfig_hostname')}."},
            },
        })
    
    return {
        'dns': dns,
    }
