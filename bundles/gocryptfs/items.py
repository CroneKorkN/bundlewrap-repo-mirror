from json import dumps

directories['/etc/gocryptfs'] = {
    'purge': True,
}

files['/etc/gocryptfs/masterkey'] = {
    'content': node.metadata.get('gocryptfs/masterkey'),
    'mode': '500',
}

files['/etc/gocryptfs/gocryptfs.conf'] = {
    'content': dumps({
    	'Version': 2,
    	'Creator': 'gocryptfs 1.6.1',
    	'ScryptObject': {
    		'Salt': node.metadata.get('gocryptfs/salt'),
    		'N': 65536,
    		'R': 8,
    		'P': 1,
    		'KeyLen': 32,
    	},
    	'FeatureFlags': [
    		'GCMIV128',
    		'HKDF',
    		'PlaintextNames',
    		'AESSIV',
    	]
    }, indent=4, sort_keys=True)
}

for path, options in node.metadata.get('gocryptfs/paths').items():
    directories[options['mountpoint']] = {
        'preceded_by': [
            f'svc_systemd:gocryptfs-{options["id"]}:stop',
        ],
        'needed_by': [
            f'svc_systemd:gocryptfs-{options["id"]}',
        ],
    }
