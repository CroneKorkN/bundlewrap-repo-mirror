{
    'dummy': True,
    'hostname': '10.0.0.16',
    'metadata': {
        'id': '3d67964d-1270-4d3c-b93f-9c44219b3d59',
        'network': {
            'internal': {
                'interface': 'eth0',
                'ipv4': '10.0.0.16/24',
                'mac': 'd8:3a:dd:16:fc:9d',
                'gateway4': '10.0.0.1',
            },
        },
        'dns': {
            'homeassistant.ckn.li': {
                'A': {
                    '10.0.0.16',
                },
            },
        },
    },
}

# LETSENCRYPT
# - cant use the letsencrypt addon, because it doesnt suppeort supplying a different zone (which would be acme.sublimity.de)

# Advanced SSH & Web Terminal:

# username: root
# password: ""
# authorized_keys:
#   - >-
#     ssh-ed25519
#     AAAAC3NzaC1lZDI1NTE5AAAAIJT9Spe+BYue7iiutl3rSf6PlU6dthHizyK+ZWnLodrA
#     root@home.server
# sftp: true
# compatibility_mode: false
# allow_agent_forwarding: false
# allow_remote_port_forwarding: false
# allow_tcp_forwarding: false

# add to /homeassistant/configuration.yaml:
# http:
#   http_port: 443 # or use nginx addon
#   ssl_certificate: /ssl/fullchain.pem
#   ssl_key: /ssl/privkey.pem
