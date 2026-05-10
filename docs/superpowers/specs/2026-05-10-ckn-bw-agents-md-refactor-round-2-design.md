# Round 2 — agent-doc refactor (gaps 7–12)

## Why

Continuation of round 1 (spec at
`2026-05-10-ckn-bw-agents-md-refactor-round-1-design.md`). Round 1
landed the cross-cutting lessons (read-only allowlist, bundle
validation needs a node, nodes-carry-only-node-specific-metadata,
reactors-must-read-metadata, triggers/triggered:True invariant,
self-healing pattern). Round 2 covers the remaining six gaps: built-in
item-type gotchas and three bundle READMEs.

## Scope

In:

- Gap 7 — `file:`'s `source` defaults to the basename of the destination.
- Gap 8 — `git_deploy` extracts as the connecting user (root after
  sudo); chown action needed for non-root downstream consumers.
- Gap 9 — `git_deploy` URL form: `://` triggers per-apply clone, no `://`
  requires a `git_deploy_repos` map at the repo root.
- Gap 10 — `bundles/letsencrypt`: first-apply behaviour, DNS-01
  prerequisites, negative-cache penalty.
- Gap 11 — `bundles/bind`: applying changes to a `master_node`-linked
  pair needs `bw apply` on both ends.
- Gap 12 — `bundles/nginx`: how port 80 is served, `vm/cores`
  requirement.

Out:

- Bundle behaviour changes. Pure docs.
- `bw apply` / `bw run` — not authorised this session.

## Placement decision (diverges from the handoff)

The handoff suggests `items/AGENTS.md` for gaps 7, 8, 9. But
`items/AGENTS.md` is scoped to **custom** item types in the `items/`
directory — its first sentence: *"Custom item types — each `*.py` is
a `bundlewrap.items.Item` subclass…"*. Built-in gotchas (`file:`,
`git_deploy:`) don't fit there.

Round-1 lessons about built-in mechanics (reactors must read metadata,
`triggers` invariant, self-healing pattern) all landed in
`bundles/AGENTS.md` Pitfalls. Gaps 7, 8, 9 are the same shape, so
they go in the same place.

## Validation findings

- Gap 7: well-known bw built-in semantics. Trusting the handoff.
- Gap 8: confirmed at `.venv/src/bundlewrap/bundlewrap/items/git_deploy.py`'s
  `fix()` method — uses `self.node.upload(...)` which writes as the sudo
  user (root). Files end up root-owned.
- Gap 9: confirmed in round 1 (`git_deploy.py:103` —
  `if "://" in self.attributes['repo']:`).
- Gap 10: confirmed `/etc/dehydrated/letsencrypt-ensure-some-certificate`
  exists in the bundle; runs on every domain with idempotent `unless`.
  Daily timer at `/usr/bin/dehydrated --cron --accept-terms --challenge dns-01`.
- Gap 11: nuanced. The bundle DOES set `bind/type = 'slave'` and renders
  different named.conf.local for slaves, so bind itself may AXFR at
  runtime. But the slave's *bw-managed* zone files are statically
  rendered from the master's metadata at slave-apply time
  (`bundles/bind/items.py:100`). The practical workflow rule — "apply
  both" — is correct regardless. I'll frame the README as the workflow
  rule, not the absolute "not AXFR slaving" claim from the handoff.
- Gap 12: confirmed `nginx.conf:42` includes `/etc/nginx/sites-enabled/*`;
  `nginx/items.py:35` reads `node.metadata.get('vm/cores')` with no
  default. README does not exist.

## Existing README states

- `bundles/letsencrypt/README.md` — 9 lines: upstream link + nsupdate
  snippet. Reshape into an operational README; keep the nsupdate snippet.
- `bundles/bind/README.md` — does not exist. Create.
- `bundles/nginx/README.md` — does not exist. Create.

## Commits

### Commit 7 — `file:` source defaults to destination basename (Gap 7)

`bundles/AGENTS.md` Pitfalls — new bullet:

```markdown
- **`file:` `source` defaults to the destination basename.** For a
  destination of `/etc/foo/bar.conf` with no `source` key, bw looks for
  `bundles/<bundle>/files/bar.conf`. Only declare `source` explicitly
  when the basename you want differs (e.g. shipping a Mako template
  named `bar.conf.mako` to a destination of `/etc/foo/bar.conf`).
```

### Commit 8 — `git_deploy` gotchas (Gaps 8 + 9)

`bundles/AGENTS.md` Pitfalls — two new bullets.

```markdown
- **`git_deploy` extracts as the connecting (sudo) user — files end up
  root-owned.** A downstream action that runs as a non-root app user
  (typical: editable pip install, Rails bundle install) will hit
  `Permission denied` on `.egg-info` or similar. The fix is a
  self-healing chown action between `git_deploy` and the downstream
  action:

  ```python
  actions['<bundle>_chown_src'] = {
      'command': 'chown -R <user>:<group> <path>',
      'unless': 'test -z "$(find <path> ! -user <user> -print -quit)"',
      'cascade_skip': False,
      'needs': ['git_deploy:<path>', 'user:<user>', 'group:<group>'],
  }
  ```

  See `bundles/left4me/items.py` for an in-tree example.

- **`git_deploy` URL form matters.** A URL containing `://` (HTTP/HTTPS,
  `ssh://`) makes bw clone to a temp dir per-apply — no operator-side
  state needed. Without `://` (SCP-style `git@host:path`), bw expects a
  `git_deploy_repos` map file at the repo root pointing at a long-lived
  local clone, and raises `RepositoryError('missing repo map for
  git_deploy')` if it isn't there. For HTTPS-reachable repos use the
  HTTPS form; for SSH-only, prefer the explicit `ssh://user@host/path`
  form so the map isn't needed.
```

### Commit 9 — letsencrypt README (Gap 10)

Reshape `bundles/letsencrypt/README.md`. Keep the upstream link and
nsupdate snippet at the top; add three structured sections.

```markdown
# letsencrypt

Issues and renews Let's Encrypt certs via [dehydrated][upstream] with
DNS-01 against the in-house bind-acme server.

[upstream]: https://github.com/dehydrated-io/dehydrated/wiki/example-dns-01-nsupdate-script

## First-apply behaviour

Immediately after `bw apply <node>`, nginx serves a **self-signed
cert** for each declared domain — generated by
`/etc/dehydrated/letsencrypt-ensure-some-certificate` so nginx has
something to start with. The real Let's Encrypt cert arrives at most
24h later when the systemd timer fires
(`/usr/bin/dehydrated --cron --accept-terms --challenge dns-01`). To
shortcut the wait:

```sh
ssh <node> 'sudo /usr/bin/dehydrated --cron --accept-terms --challenge dns-01'
ssh <node> 'sudo systemctl reload nginx'
```

## DNS-01 prerequisites

`hook.sh` does `nsupdate` against the bind-acme server (referenced
by `letsencrypt/acme_node`). For the challenge to succeed:

1. The acme node must be in the same metadata graph (so
   `bw metadata <node> -k letsencrypt/acme_node` resolves).
2. **All NS servers** for the validated domain must serve the
   `_acme-challenge.<domain>` CNAME — Let's Encrypt validates from
   primary AND secondary geographic regions; both authoritative
   servers must agree. If a secondary NS is also a bw-managed node,
   `bw apply` it after adding the domain (see e.g. `ovh.secondary`).
3. The bind-acme node's TSIG key must be reachable. `hook.sh` is
   rendered with the bind-acme server's `network/internal/ipv4` —
   for clients outside that LAN, the route must exist (typically via
   wireguard `s2s` peer membership).

## Negative-cache penalty

If the first DNS-01 attempt fails (e.g. zone not yet applied to the
secondary NS), Let's Encrypt's resolvers cache NXDOMAIN for the SOA's
negative TTL (often 900s = 15 min). Subsequent attempts during that
window also fail and refresh the cache. Combined with LE's rate limit
of **5 failed authorisations per domain per hour**, recovery requires
you to **stop retrying** for ~15 minutes after fixing the DNS, then
make at most one attempt.

## nsupdate sample

For interactive testing of the bind-acme TSIG path:

```sh
printf "server 127.0.0.1
zone acme.resolver.name.
update add _acme-challenge.ckn.li.acme.resolver.name. 600 IN TXT \"hello\"
send
" | nsupdate -y hmac-sha512:acme:<TSIG_KEY_REDACTED>
```
```

### Commit 10 — bind README (Gap 11, reframed)

Create `bundles/bind/README.md`. Frame as the workflow rule, not the
absolute "not AXFR" claim.

```markdown
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
  negative-cache penalty (the most common operational consequence of
  forgetting to apply the secondary).
```

### Commit 11 — nginx README (Gap 12)

Create `bundles/nginx/README.md`.

```markdown
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
specific port-80 behaviour (e.g. plain-HTTP without redirect), you'll
need to override 80.conf or add a per-vhost block.

## Required metadata

- `vm/cores` — read directly by `items.py` for `worker_processes`.
  No default; `bw items <node>` raises at item-build time if missing.
  Typically supplied by the `vm` bundle / hetzner-vm group; double-
  check on bare-metal hosts.
- `nginx/vhosts` — dict of vhost-name → vhost-config.
- `nginx/modules` — list of dynamic modules to load.

## Cross-namespace

`items.py` reads `letsencrypt/domains` to skip emitting a per-vhost
HTTPS block when LE hasn't declared the domain yet — keeps the bundle
loadable on a node where letsencrypt isn't fully wired up.
```

## Out of scope

- Bundle behaviour changes. Pure docs.
- `bw apply` / `bw run`.
- Reformatting the existing two-line bundle READMEs into the new
  shape — bundles/AGENTS.md explicitly says don't do that
  ("uneven quality is part of what we accept in exchange for not
  blocking other work").

## Constraints

- Don't echo decrypted secrets. The TSIG-key example in the
  letsencrypt nsupdate snippet uses `<TSIG_KEY_REDACTED>`.
- After each commit, `.venv/bin/bw test` must pass.
- No push.
