dm-crypt
========

Create encrypted block devices using `dm-crypt` on GNU/Linux. Unlocking
these devices will be done on runs of `bw apply`.

Metadata
--------

    'dm-crypt': {
        'encrypted-devices': {
            'foobar': {
                'device': '/dev/sdb',
                # either
                'salt': 'muWWU7dr+5Wtk+56OLdqUNZccnzXPUTJprMSMxkstR8=',
                # or
                'password': vault.decrypt('passphrase'),
            },
        },
    },

This will encrypt `/dev/sdb` using the specified passphrase. When the
device is going to be unlocked, it will be available as
`/dev/mapper/foobar`.
