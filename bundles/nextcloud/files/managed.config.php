<?php
# https://docs.nextcloud.com/server/stable/admin_manual/configuration_server/config_sample_php_parameters.html#multiple-config-php-file
$CONFIG = array (
  'dbuser' => 'nextcloud',
  'dbpassword' => '${db_password}',
  'dbname' => 'nextcloud',
  'dbhost' => 'localhost',
  'dbtype' => 'pgsql',
  'datadirectory' => '/var/lib/nextcloud',
  'dbport' => '5432',
);
