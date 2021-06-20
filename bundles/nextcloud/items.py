assert node.has_bundle('php')

version = node.metadata.get('nextcloud/version')

downloads[f'/tmp/nextcloud-{version}.tar.bz2'] = {
    'url': f'https://download.nextcloud.com/server/releases/nextcloud-{version}.tar.bz2',
    'sha256': node.metadata.get('nextcloud/sha256'),
    'triggered': True,
}

directories['/opt/nextcloud'] = {}

actions['extract_nextcloud'] = {
    'command': f'tar xfvj /tmp/nextcloud-{version}.tar.bz2 --strip 1 -C /opt/nextcloud nextcloud',
    'unless': f"""php -r 'include "/opt/nextcloud/version.php"; echo "$OC_VersionString";' | grep -q '^{version}$'""",
    'preceded_by': [
        f'download:/tmp/nextcloud-{version}.tar.bz2',
    ],
    'needs': [
        'directory:/opt/nextcloud',
    ],
}

directories['/var/lib/nextcloud'] = {
    'owner': 'www-data',
    'group': 'www-data',
}
