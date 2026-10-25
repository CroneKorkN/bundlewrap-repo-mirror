# Mail server move: htz.mails → ovh.mails

htz.mails (2 vCPU, 3.8 GB RAM, mail on a Hetzner network volume) cannot be
upgraded at a sensible price. ovh.mails (OVH VPS-1: 4 vCPU, 7.7 GB RAM,
75 GB local disk) takes over all of its roles; htz.mails becomes the DNS
secondary or is shut down.

Measured on 2026-10-25, 4k random reads at queue depth 1: 626 IOPS on the
Hetzner volume, 7,896 on the OVH disk; 4k fsync writes 227 vs 10,835.

## Rules until the switchover

- **No bind apply anywhere** (htz.mails, home.router, ovh.mails): the zones
  are built from all nodes' metadata and would already list the OVH
  addresses. Partial applies use `-s bundle:bind`.
- No full `bw apply` on these three nodes.
- `secondary.resolver.name` does not answer until the switchover.

## Done

- [x] OVH reinstalled with Debian 13, root shrunk to 20 GB, `sda2` with
      partlabel `tank` (~55 GB)
- [x] Cloud kernel replaced by the generic one (zfs-dkms builds against it)
- [x] `nodes/ovh.mails.py` (renamed from ovh.secondary, same id): all roles
      of htz.mails, but bind slave of htz.mails, wireguard peer, no backup,
      no 10.0.10.2, no bind-acme; marked `FIXME`
- [x] First apply with `-s bundle:bind`, 0 failed
- [x] Pool `tank` recreated with ashift 12, `dnodesize=auto`
- [x] Record sizes: vmail 128K, vmail/index 8K
- [x] Initial transfer: snapshots `@migrate1` on htz.mails, `zfs send -c`
      per dataset through wireguard into `zfs recv -u` on ovh.mails
      (`/tmp/migrate-send.sh` on htz.mails, units `migrate-recv-900x` on
      ovh.mails, nft rule for tcp 9001-9007 on wg0 in memory only)

## Phase 2: test before the switchover

1. `bw apply ovh.mails -o bundle:zfs` for mountpoints and properties.
2. Start the services on ovh.mails, check mailboxes, postgres, mariadb,
   wordpress.
3. Test from the Mac with `/etc/hosts`: `51.68.189.180 mail.sublimity.de`
   - Roundcube login and timings
   - IMAP from the phone
   - SMTP send to mail-tester.com

## Phase 3: switchover (30-60 min maintenance)

1. htz.mails: stop postfix, dovecot, rspamd, php8.4-fpm, nginx, postgresql,
   mariadb, redis-server, redis-rspamd.
2. On ovh.mails `zfs rollback -r` every dataset to `@migrate1`, dropping
   the test changes and auto-snapshots since. Snapshot `@migrate2` on all
   seven datasets on htz.mails, `zfs send -c -i @migrate1` into them.
3. Rewrite the mail data so it gets the new record sizes; `zfs send` keeps
   the block sizes of the sender (vmail 16K, index 4K), neither `-L`,
   `recv -o` nor `zfs rewrite` change them. On ovh.mails, services still
   stopped, for `tank/vmail` and `tank/vmail/index`:
   - `zfs rename` the received dataset to `…-received`, unmount it
   - create the dataset anew with the bundle properties (vmail now zstd)
   - `cp -a` the content over (local NVMe, a few minutes for ~20 GB)
   - destroy `…-received` after a check
4. Repo:
   - ovh.mails: bind master, `bind-acme`, backup group, `internal` dummy
     with 10.0.10.2, wireguard hub with the peers and clients of htz.mails,
     the hardcoded A/AAAA of ckn.li, sublimity.de, freibrief.net
   - htz.mails → htz.secondary (same id): bind slave of ovh.mails,
     wireguard peer, without the mail roles
   - all references to htz.mails: `acme_node` (groups/os/linux.py),
     `master_node` (home.router), `download_server` (home.server),
     wireguard peers (home.router, mseibert.*), `bin/wireguard-client-config`
5. Apply ovh.mails, htz.secondary, home.router, mseibert.freescout,
   mseibert.yourls, home.server.
6. Providers:
   - INWX: glue `resolver.name` → OVH, `secondary.resolver.name` → Hetzner
   - OVH: PTR 51.68.189.180 and 2001:41d0:701:1100::751a → mail.sublimity.de
   - Hetzner: PTR to the new name
7. By hand: wireguard endpoint on wb.offsite-backups and ovh.left4me
   (dummy nodes), new QR codes for macbook, phone, ipad.
8. Remove the nft rule and the `@migrate*` snapshots.

## Phase 4: afterwards

- Monitoring, first nightly backup, DMARC reports and delivery to Gmail.
- Measure Roundcube again.
- After one or two weeks: keep htz.secondary or shut it down (then a second
  nameserver, e.g. OVH secondary DNS).
- Move the resolver to the wireguard ip 172.30.0.1 and drop 10.0.10.0/24
  with the dummy interface.

## Rollback

Until step 6 htz.mails stays untouched apart from stopped services: start
them again and do not apply the repo changes. Mail delivered to ovh.mails
in the meantime has to be copied back by hand.
