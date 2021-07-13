assert node.has_bundle('systemd')

files = {
    '/etc/network/interfaces': {
        'delete': True,
    },
}

files['/etc/resolv.conf'] = {
    'content_type': 'mako',
}

directories = {
    '/etc/systemd/network': {
        'purge': True,
    },
}

# for type, path in {
#     'networks': '/etc/systemd/network/{}.network',
#     'netdevs': '/etc/systemd/network/{}.netdev',
# }.items():
#     for name, config in node.metadata.get(f'systemd-networkd/{type}').items():
#         files[path.format(name)] = {
#             'content': repo.libs.systemd.generate_unitfile(config),
#             'needed_by': {
#                 'svc_systemd:systemd-networkd',
#             },
#             'triggers': {
#                 'svc_systemd:systemd-networkd:restart',
#             },
#         }
# 
svc_systemd = {
    'systemd-networkd': {},
}
