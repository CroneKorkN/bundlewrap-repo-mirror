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

Branch `mail-ovh-switch` holds the repo side: ovh.mails as bind master,
wireguard hub, acme node and resolver (10.0.10.2 on a dummy), htz.mails
renamed to htz.secondary (bind slave, wireguard peer, no mail roles), all
references repointed. Nodes whose config changes (`bw hash` against
master): ovh.mails, htz.secondary, home.router, home.backups,
mseibert.freescout, mseibert.yourls; by hand: wb.offsite-backups,
ovh.left4me.

1. htz.mails: `systemctl disable --now` postfix, dovecot, rspamd,
   opendkim, php8.4-fpm, nginx, postgresql, mariadb, redis-server,
   redis-rspamd; senders queue and retry.
2. ovh.mails: stop the same services, `zfs rollback -r tank/<ds>@migrate1`
   for all seven datasets (drops test changes and auto-snapshots).
3. htz.mails: `zfs snapshot` `@migrate2` on all seven, send
   `zfs send -c -i @migrate1 <ds>@migrate2` through wireguard into
   `zfs recv -u` on ovh.mails (same nc scheme, ports 9001-9007).
4. ovh.mails, rewrite for the new record sizes (`zfs send` keeps the
   sender's block sizes, neither `-L`, `recv -o` nor `zfs rewrite` change
   them):
   - `zfs rename tank/vmail/index tank/index-received`,
     `zfs rename tank/vmail tank/vmail-received`, both to `/mnt/…-received`
   - `zfs create` `tank/vmail` (zstd, 128K, atime off, `/var/vmail`) and
     `tank/vmail/index` (8K, atime off, no auto-snapshot, `/var/vmail/index`)
   - `cp -a` both contents over, compare file counts, destroy `…-received`
5. ovh.mails: remap file owners from the htz ids to the local ones, exactly
   once and before any apply (`/tmp/remap_ids.py`, map built by user and
   group name; a second run would remap the already local ids).
6. Merge the branch, push.
7. Apply ovh.mails (now with bind), then htz.secondary, home.router,
   mseibert.freescout, mseibert.yourls, home.backups (wake it first).
   On htz.secondary check that 10.0.10.2 is gone from the private network
   interface, otherwise remove the old `internal.network` unit.
8. Providers (Martin):
   - INWX: glue `resolver.name` → 51.68.189.180 / 2001:41d0:701:1100::751a,
     `secondary.resolver.name` → 49.12.184.229 / 2a01:4f8:c013:51f2::1
   - OVH: PTR 51.68.189.180 and 2001:41d0:701:1100::751a → mail.sublimity.de
   - Hetzner: PTR to secondary.htz.ckn.li
9. By hand: wireguard on wb.offsite-backups and ovh.left4me (new endpoint
   and hub key), new QR codes for macbook, phone, ipad
   (`bin/wireguard-client-config`).
10. Remove the nft rule for 9001-9007 and the `@migrate*` snapshots, the
    `/etc/hosts` test entries (ovh.mails, Mac).

The acme tsig key that leaked into a session transcript derives from the
master's id, so it changes with the new master; the old one stops working
once htz.secondary runs as slave.

## Phase 4: afterwards

- Monitoring, first nightly backup, DMARC reports and delivery to Gmail,
  a send test to mail-tester.com.
- Measure Roundcube again.
- Optimize: Roundcube `imap_cache` and `messages_cache`, measured before and
  after. Old spam and the inbox stay as they are.
- After one or two weeks: keep htz.secondary or shut it down (then a second
  nameserver, e.g. OVH secondary DNS).
- Move the resolver to the wireguard ip 172.30.0.1 and drop 10.0.10.0/24
  with the dummy interface.

## Rollback

Until step 6 htz.mails stays untouched apart from stopped services: enable
and start them again and do not merge the branch. Mail delivered to ovh.mails
in the meantime has to be copied back by hand.
