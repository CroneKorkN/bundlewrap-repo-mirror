# bind

Authoritative DNS — primary plus optional `bind/master_node` slaves.

## Applying changes needs both nodes

The slave's bw-managed zone files are rendered from the master's
metadata at slave-apply time (see `bundles/bind/items.py:100`). When
you change a record on the master (adding a `letsencrypt/domains`
entry, a new vhost, etc.), the change is only published once you
apply BOTH:

```sh
bw apply htz.mails        # primary (where the source records live)
bw apply ovh.secondary    # secondary (renders its own zone files)
```

Until both have been applied, `bw verify ovh.secondary` will show
stale zones and consumers that hit the secondary (Let's Encrypt's
secondary-region validators in particular) will see NXDOMAIN. Even
though the slave's named.conf.local declares `type slave;`, don't
rely on bind's own AXFR catching up — the bw-rendered file on disk
is what `bw verify` measures.

## See also

- `bundles/bind-acme/` — the in-house ACME-update receiver.
- `bundles/letsencrypt/README.md` — DNS-01 prerequisites and the
  negative-cache penalty (the most common operational consequence
  of forgetting to apply the secondary).
