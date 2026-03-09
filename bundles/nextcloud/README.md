Nextcloud
=========

import iphone pictures
----------------------

Use Photos app on macOS
- select library in the left sidebar
- select the pictures
- in menu bar open File > Export Unmodified Original for X Photos

The only reliable way to get some files creation time is being lost with rsync, so
we need to embed those timestamps on macos first:

```sh
PHOTOS_PATH="/Users/mwiegand/Desktop/photos"
bin/timestamp_icloud_photos_for_nextcloud -d "$PHOTOS_PATH"
rsync -avh --progress --rsync-path="sudo rsync" "$PHOTOS_PATH/" ckn@10.0.0.2:/var/lib/nextcloud/ckn/files/SofortUpload/AutoSort/
```

preview generator
-----------------

```
sudo -u www-data php /opt/nextcloud/occ preview:generate-all -w "$(nproc)" -n -vvv
```

This index speeds up preview generator dramatically:
```sh
CREATE INDEX CONCURRENTLY oc_filecache_path_hash_idx
ON oc_filecache (path_hash);
```

delete previews:
```sh
psql nextcloud -x -c "DELETE FROM oc_previews;"
rm -rf /var/lib/nextcloud/appdata_oci6dw1woodz/preview/*
```

https://docs.nextcloud.com/server/stable/admin_manual/configuration_files/previews_configuration.html#maximum-preview-size
```php
    'preview_max_x' => 1920,
    'preview_max_y' => 1920,
    'preview_max_scale_factor' => 4,
```

https://github.com/nextcloud/previewgenerator?tab=readme-ov-file#i-dont-want-to-generate-all-the-preview-sizes
```sh
sudo -u www-data php /opt/nextcloud/occ config:app:set --value="64 256" previewgenerator squareSizes
sudo -u www-data php /opt/nextcloud/occ config:app:set --value="" previewgenerator fillWidthHeightSizes # changed
sudo -u www-data php /opt/nextcloud/occ config:app:set --value="" previewgenerator widthSizes
sudo -u www-data php /opt/nextcloud/occ config:app:set --value="" previewgenerator heightSizes
sudo -u www-data php /opt/nextcloud/occ config:app:set preview jpeg_quality --value="75"
sudo -u www-data php /opt/nextcloud/occ config:app:set --value=0 --type=integer previewgenerator job_max_previews # in favour of systemd timer
```

gen previews
```sh
php /opt/nextcloud/occ preview:generate-all --workers="$(nproc)" --no-interaction -vvv
```

check preview geenration
```sh
find /var/lib/nextcloud/appdata_oci6dw1woodz/preview
# /var/lib/nextcloud/appdata_oci6dw1woodz/preview/6/9/1/f/7/b/4/2822419/64-64-crop.jpg
# /var/lib/nextcloud/appdata_oci6dw1woodz/preview/6/9/1/f/7/b/4/2822419/256-256-crop.jpg
# /var/lib/nextcloud/appdata_oci6dw1woodz/preview/6/9/1/f/7/b/4/2822419/1280-1920-max.jpg

du -sh /var/lib/nextcloud/appdata_oci6dw1woodz/preview
# 28G	/var/lib/nextcloud/appdata_oci6dw1woodz/preview
```