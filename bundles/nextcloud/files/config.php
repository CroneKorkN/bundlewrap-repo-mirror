<?php
$CONFIG = array (
  'instanceid' => 'ocfnc48njsxw',
  'passwordsalt' => 'xxx',
  'secret' => 'xxx',
  'trusted_domains' =>
  array (
    0 => 'cloud.sublimity.de',
  ),
  'trusted_proxies' =>
  array (
    0 => 'cloud.sublimity.de',
  ),
  'datadirectory' => '/var/lib/nextcloud',
  'overwrite.cli.url' => 'https://cloud.sublimity.de',
  'overwriteprotocol' => 'https',
  'dbtype' => 'mysql',
  'version' => '21.0.1.1',
  'dbname' => 'nextcloud',
  'dbhost' => 'localhost',
  'dbport' => '',
  'dbtableprefix' => 'oc_',
  'dbuser' => 'nextcloud',
  'dbpassword' => 'xxx',
  'installed' => true,
  'updater.release.channel' => 'stable',
  'maintenance' => false,
  'memcache.local' => '\\OC\\Memcache\\Redis',
  'memcache.locking' => '\\OC\\Memcache\\Redis',
  'theme' => '',
  'default_phone_region' => 'DE',
  'loglevel' => 0,
  'preview_max_x' => 1280,
  'preview_max_y' => 1280,
  'preview_max_scale_factor' => 1,
  'user_backends' =>
  array (
    0 =>
    array (
      'class' => 'OC_User_IMAP',
      'arguments' =>
      array (
        0 => '{mail.sublimity.de:143}',
      ),
    ),
  ),
  'mail_smtpmode' => 'smtp',
  'mail_smtpauthtype' => 'PLAIN',
  'mail_smtpsecure' => 'tls',
  'mail_from_address' => 'cloud',
  'mail_domain' => 'sublimity.de',
  'mail_smtphost' => 'mail.sublimity.de',
  'mail_smtpport' => '587',
  'mail_smtpauth' => 1,
  'mail_smtpname' => 'xxx',
  'mail_smtppassword' => 'xxx',
  'mysql.utf8mb4' => true,
  'app_install_overwrite' =>
  array (
    0 => 'spreed',
    1 => 'camerarawpreviews',
    2 => 'calendar',
    3 => 'previewgenerator',
  ),
);
