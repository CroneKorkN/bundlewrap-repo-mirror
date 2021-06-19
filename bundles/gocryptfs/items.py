from hashlib import sha3_256
from base64 import b64decode, b64encode
from binascii import hexlify
from uuid import UUID
from json import dumps

id = node.metadata.get('id')

directories['/etc/gocryptfs'] = {
    'purge': True,
}

files['/etc/gocryptfs/masterkey'] = {
    'content': hexlify(b64decode(
        str(repo.vault.random_bytes_as_base64_for(id, length=32))
    )),
    'mode': '500',
}

files['/etc/gocryptfs/gocryptfs.conf'] = {
    'content': dumps({
    	'Version': 2,
    	'Creator': 'gocryptfs 1.6.1',
    	'ScryptObject': {
    		'Salt': b64encode(
                sha3_256(UUID(id).bytes).digest()
            ).decode(),
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
