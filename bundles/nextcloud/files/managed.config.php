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
  "upgrade.disable-web" => true,
  "memcache.local" => "\\OC\\Memcache\\Redis",
  "memcache.locking" => "\\OC\\Memcache\\Redis",
  "memcache.distributed" => "\OC\Memcache\Redis",
  "redis" => [
    "host" => "/var/run/redis/nextcloud.sock",
  ],
  'trusted_domains' =>
  array (
    0 => 'localhost',
    1 => '127.0.0.1',
    2 => '${hostname}',
  ),
  "log_type" => "syslog",
  "syslog_tag" => "nextcloud",
  "logfile" => "",
  "loglevel" => 3,
  "default_phone_region" => "DE",
  "versions_retention_obligation" => "auto, 90",
  'simpleSignUpLink.shown' => false,
);
