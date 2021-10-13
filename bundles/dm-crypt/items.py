for name, conf in node.metadata.get('dm-crypt').items():
    actions[f'dm-crypt_format_{name}'] = {
        'command': f"cryptsetup --batch-mode luksFormat --cipher aes-xts-plain64 --key-size 512 '{conf['device']}'",
        'data_stdin': conf['password'],
        'unless': f"blkid -t TYPE=crypto_LUKS '{conf['device']}'",
        'comment': f"WARNING: This DESTROYS the contents of the device: '{conf['device']}'",
        'needs': {
            'pkg_apt:cryptsetup',
        },
    }
    
    actions[f'dm-crypt_test_{name}'] = {
        'command': 'false',
        'unless': f"! cryptsetup --batch-mode luksOpen --test-passphrase '{conf['device']}'",
        'data_stdin': conf['password'],
        'needs': {
            f"action:dm-crypt_format_{name}",
        },
    }
    
    actions[f'dm-crypt_open_{name}'] = {
        'command': f"cryptsetup --batch-mode luksOpen '{conf['device']}' '{name}'",
        'data_stdin': conf['password'],
        'unless': f"test -e /dev/mapper/{name}",
        'comment': f"Unlocks the device '{conf['device']}' and makes it available in: '/dev/mapper/{name}'",
        'needs': {
            f"action:dm-crypt_test_{name}",
        },
        'needed_by': set(),
    }

    if node.has_bundle('zfs'):
        for pool, pool_conf in node.metadata.get('zfs/pools').items():
            if f'/dev/mapper/{name}' in pool_conf['devices']:
                actions[f'dm-crypt_open_{name}']['needed_by'].add(f'zfs_pool:{pool}')
