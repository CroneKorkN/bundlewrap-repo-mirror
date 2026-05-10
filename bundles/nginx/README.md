# nginx

Webserver. Per-node vhosts in `nginx/vhosts`; per-vhost templates in
`data/nginx/*.conf`.

## How port 80 is served

The bundle ships a fixed `80.conf` to
`/etc/nginx/sites-available/80.conf` (picked up by the
`sites-enabled/` symlink) that handles **all** port-80 traffic
across vhosts:

1. ACME HTTP-01 challenges (`/.well-known/acme-challenge/`) are
   served from `/var/lib/dehydrated/acme-challenges/`.
2. All other port-80 requests are 301-redirected to
   `https://$host$request_uri`.

Per-vhost templates only declare `listen 443 ssl http2;`, so they
don't need their own port-80 server blocks. If you need vhost-
specific port-80 behaviour (e.g. plain-HTTP without redirect),
override 80.conf or add a per-vhost block.

## Required metadata

- `vm/cores` — read directly by `items.py` for `worker_processes`.
  No default; `bw items <node>` raises at item-build time if missing.
  Typically supplied by the `vm` bundle / hetzner-vm group; double-
  check on bare-metal hosts.
- `nginx/vhosts` — dict of vhost-name → vhost-config.
- `nginx/modules` — list of dynamic modules to load.

## Cross-namespace

`items.py` reads `letsencrypt/domains` to skip emitting a per-vhost
HTTPS block when LE hasn't declared the domain yet — keeps the
bundle loadable on a node where letsencrypt isn't fully wired up.
