defaults = {
    'apt': {
        'packages': {
            'libnginx-mod-stream': {},
            'libnginx-mod-rtmp': {},
        },
    },
    'nftables': {
        'input': {
            'tcp dport 1936 accept',
        },
    },
    'nginx': {
        'modules': {
            'rtmp',
            'stream',
        },
    },
}


@metadata_reactor.provides(
    'nginx-rtmps/stream_key',
)
def stream_key(metadata):
    return {
        'nginx-rtmps': {
            'stream_key': repo.vault.password_for(f"{metadata.get('id')} nginx-rtmps stream_key", length=24)
        },
    }


@metadata_reactor.provides(
    'dns',
)
def dns(metadata):
    return {
        'dns': {
            metadata.get('nginx-rtmps/hostname'): repo.libs.ip.get_a_records(metadata),
        }
    }


@metadata_reactor.provides(
    'letsencrypt/domains',
)
def letsencrypt(metadata):
    return {
        'letsencrypt': {
            'domains': {
                metadata.get('nginx-rtmps/hostname'): {
                    'reload': {'nginx'},
                },
            },
        },
    }
