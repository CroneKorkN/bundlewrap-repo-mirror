defaults = {
    'left4me': {
        'gunicorn_workers': 1,
        'gunicorn_threads': 32,
        'job_worker_threads': 4,
        'port_range_start': 27015,
        'port_range_end': 27115,
    },
    'apt': {
        'packages': {
            'p7zip-full': {},
            'nftables': {},
            'iproute2': {},
            'curl': {},
            'ca-certificates': {},
        },
    },
}
