from hashlib import sha3_256
from base64 import b64decode, b64encode
from binascii import hexlify
from uuid import UUID

defaults = {
    'apt': {
        'packages': {
            'gocryptfs': {},
            'fuse': {},
            'socat': {},
        },
    },
    'gocryptfs': {
        'paths': {},
    },
}


@metadata_reactor.provides(
    'gocryptfs',
)
def config(metadata):
    return {
        'gocryptfs': {
            'masterkey': hexlify(b64decode(
                str(repo.vault.random_bytes_as_base64_for(metadata.get('id'), length=32))
            )).decode(),
            'salt': b64encode(
                sha3_256(UUID(metadata.get('id')).bytes).digest()
            ).decode(),
        },
    }


@metadata_reactor.provides(
    'gocryptfs',
)
def paths(metadata):
    paths = {}
    
    for path, options in metadata.get('gocryptfs/paths').items():
        paths[path] = {
            'id': hexlify(sha3_256(path.encode()).digest()[:8]).decode(),
        }
    
    return {
        'gocryptfs': {
            'paths': paths,
        },
    }



@metadata_reactor.provides(
    'systemd/services',
)
def systemd(metadata):
    services = {}
    
    for path, options in metadata.get('gocryptfs/paths').items():
        services[f'gocryptfs-{options["id"]}'] = {
            'content': {
                'Unit': {
                    'Description': f'gocryptfs@{path} ({options["id"]})',
                    'After': {
                      'filesystem.target',
                      'zfs.target',
                    },
                },
                'Service': {
                    'RuntimeDirectory': 'gocryptfs',
                    'Environment': {
                        'MASTERKEY': metadata.get('gocryptfs/masterkey'),
                        'SOCKET': f'/var/run/gocryptfs/{options["id"]}',
                        'PLAIN': path,
                        'CIPHER': options["mountpoint"]
                    },
                    'ExecStart': [
                        '/usr/bin/gocryptfs -fg -plaintextnames -reverse -masterkey $MASTERKEY -ctlsock $SOCKET $PLAIN $CIPHER',
                    ],
                    'ExecStopPost': [
                        '/usr/bin/umount $CIPHER'
                    ],
                },
            },
            'needs': [
                'pkg_apt:gocryptfs',
                'pkg_apt:fuse',
                'pkg_apt:socat',
                'file:/etc/gocryptfs/masterkey',
                'file:/etc/gocryptfs/gocryptfs.conf',
            ],
            'triggers': [
                f'svc_systemd:gocryptfs-{options["id"]}:restart',
            ],
        }

    return {
        'systemd': {
            'services': services,
        },
    }
