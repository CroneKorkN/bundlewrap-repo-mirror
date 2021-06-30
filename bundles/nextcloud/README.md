# downloads[f'/tmp/nextcloud-{version}.tar.bz2'] = {
#     'url': f'https://download.nextcloud.com/server/releases/nextcloud-{version}.tar.bz2',
#     'sha256_url': '{url}.sha256',
#     'triggered': True,
# }
# actions['delete_nextcloud'] = {
#     'command': 'rm -rf /opt/nextcloud/*',
#     'triggered': True,
# }
# actions['extract_nextcloud'] = {
#     'command': f'tar xfvj /tmp/nextcloud-{version}.tar.bz2 --strip 1 -C /opt/nextcloud nextcloud',
#     'unless': f"""php -r 'include "/opt/nextcloud/version.php"; echo "$OC_VersionString";' | grep -q '^{version}$'""",
#     'preceded_by': [
#         'action:delete_nextcloud',
#         f'download:/tmp/nextcloud-{version}.tar.bz2',
#     ],
#     'needs': [
#         'directory:/opt/nextcloud',
#     ],
# }


# git_deploy = {
#     '/opt/nextcloud': {
#         'repo': 'git://github.com/nextcloud/server.git',
#         'rev': f"v{node.metadata.get('nextcloud/version')}",
#         'needs': {
#             'directory:/opt/nextcloud',
#         },
#     },
#     '/opt/nextcloud/3rdparty': {
#         'repo': 'git://github.com/nextcloud/3rdparty.git',
#         'rev': f"v{node.metadata.get('nextcloud/version')}",
#         'needs': {
#             'git_deploy:/opt/nextcloud',
#         },
#     },
# }
