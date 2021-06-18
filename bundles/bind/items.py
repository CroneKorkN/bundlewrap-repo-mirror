# for zone, records in node.metadata.get('bind/zones').items():
#     files[f'/var/lib/bind/{zone}'] = {
#         'source': 'zonefile',
#         'content_type': 'mako',
#         'context': {
#             'records': records,
#         }
#     }
