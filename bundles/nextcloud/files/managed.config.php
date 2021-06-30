<?php
# https://docs.nextcloud.com/server/stable/admin_manual/configuration_server/config_sample_php_parameters.html#multiple-config-php-file
$CONFIG = array (
  "dbuser" => "nextcloud",
  "dbpassword" => "${db_password}",
  "dbname" => "nextcloud",
  "dbhost" => "localhost",
  "dbtype" => "pgsql",
  "datadirectory" => "/var/lib/nextcloud",
  "dbport" => "5432",
  "apps_paths" => [
    [
      "path"     => "/opt/nextcloud/apps",
      "url"      => "/apps",
      "writable" => false,
    ],
    [
      "path"     => "/var/lib/nextcloud/.userapps",
      "url"      => "/userapps",
      "writable" => true,
    ],
  ],
  "cache_path" => "/var/lib/nextcloud/.cache",
);
