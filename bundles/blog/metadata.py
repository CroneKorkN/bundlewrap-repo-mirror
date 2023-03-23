from ipaddress import ip_interface

defaults = {
    'flask': {
        'blog' : {
            'git_url': "https://git.sublimity.de/cronekorkn/flask-blog.git",
            'port': 5010,
            'app_module': 'blog',
            'env': {
                'DATA_PATH': '/var/blog',
            },
        },
    },
    'users': {
        'blog': {},
    },
}


@metadata_reactor.provides(
    'nginx/vhosts',
)
def nginx(metadata):
    return {
        'nginx': {
            'vhosts': {
                metadata.get('blog/hostname'): {
                    'content': 'nginx/proxy_pass.conf',
                    'context': {
                        'target': 'http://127.0.0.1:5010',
                    },
                },
            },
        },
    }
