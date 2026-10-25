# Nextcloud: mount the user datasets one level up

## Goal

`hdd/nextcloud/ckn` and `hdd/nextcloud/ckn-privat` are mounted at
`/var/lib/nextcloud/<user>/files`. Their `cache`, `uploads`, `files_versions`
and `files_trashbin` live on the parent `hdd/nextcloud`, so assembling chunked
uploads, writing versions and deleting into the trash copy across datasets.
Mounted at `/var/lib/nextcloud/<user>`, all of these become renames, and the
trash bin can be enabled again.

- Paths as nextcloud sees them stay the same: no filecache change, file ids,
  shares, tags and recognize results survive.
- Nothing moves to another pool; `hdd/nextcloud` is on the hdd pool as well.
- Other users live directly on `hdd/nextcloud` and are not affected.

## Inventory (2026-10-25)

| | ckn | ckn-privat |
|---|---|---|
| used | 2.46T | 259G |
| entries in the dataset root | 19 (one dotfile) | 183 (`.htaccess`) |
| next to `files/` on the parent | cache, files_versions, uploads (< 1M) | cache, files_versions, uploads, files_trashbin (133M) |
| name collisions in the root (`files`, `cache`, `uploads`, `files_*`) | none | none |

Nothing else references the user paths: picsort and the rsync recipe in
`bundles/nextcloud/README.md` use `/var/lib/nextcloud/<user>/files/...`,
which stays valid.

## Runbook

Takes minutes; recognize only pauses, its queues survive.

### 0. Pause

```sh
OCC="sudo -u www-data php /opt/nextcloud/occ"
sudo systemctl stop recognize-worker-imagenet recognize-worker-faces recognize-worker-media
sudo systemctl stop nextcloud-cron.timer nextcloud-generate-new-previews.timer nextcloud-picsort-ckn.timer nextcloud-scan-files.timer
while pgrep -f /opt/nextcloud/cron.php; do sleep 10; done
$OCC maintenance:mode --on
sudo zfs snapshot hdd/nextcloud@before-remount
sudo zfs snapshot hdd/nextcloud/ckn@before-remount
sudo zfs snapshot hdd/nextcloud/ckn-privat@before-remount
```

### 1. Per user (`U=ckn`, then `U=ckn-privat`)

```sh
U=ckn
D=/var/lib/nextcloud/$U
sudo zfs umount hdd/nextcloud/$U
sudo mv $D $D.old
sudo zfs set mountpoint=$D hdd/nextcloud/$U
sudo mkdir $D/.files-new
sudo find $D -mindepth 1 -maxdepth 1 ! -name .files-new -exec mv -t $D/.files-new {} +
sudo mv $D/.files-new $D/files
sudo rmdir $D.old/files
# globs as root, the agent user cannot list these directories
sudo bash -c "mv $D.old/* $D/"
sudo rmdir $D.old
sudo chown www-data:www-data $D $D/files
sudo chmod 0770 $D
```

### 2. Repo

`nodes/home.server.py`: mountpoints to `/var/lib/nextcloud/ckn` and
`/var/lib/nextcloud/ckn-privat`; `bw verify home.server -o bundle:zfs` must be
clean, no apply needed.

### 3. Resume and check

```sh
$OCC maintenance:mode --off
$OCC files:scan ckn ckn-privat     # expect no new or removed files
sudo systemctl start nextcloud-cron.timer nextcloud-generate-new-previews.timer nextcloud-picsort-ckn.timer nextcloud-scan-files.timer
```

Restart the recognize workers (same `systemd-run` calls as before).
Upload a large file in the browser and check it lands in `files/`.

### 4. Trash bin

- `occ app:enable files_trashbin`.
- Retention in the nextcloud config of the repo, e.g.
  `'trashbin_retention_obligation': 'auto, 30'`, so the trash does not fill
  the disk.
- Test: delete a large file, it must vanish instantly and show up in the trash.

## Rollback

Before step 3, per user: `zfs umount`, `zfs set mountpoint=.../<user>/files`,
then `zfs rollback` all three `@before-remount` snapshots, which also undoes
the `.old` rename on the parent. The snapshots go once everything works.

## Afterwards

Snapshots older than the move hold the user files in their root, newer ones
under `files/`: restores from `.zfs/snapshot` need the right path.
