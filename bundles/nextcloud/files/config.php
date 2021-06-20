<?php
$CONFIG = array (
  'instanceid' => '${instance_id}',
% if not setup:
  'passwordsalt' => 'jySy/iELFRob7rRpecEXAI2Rn1gbNI',
  'secret' => 'wj3r+B2/NS8X/ETWCTnwwrNy+dyy2OSWRCVQxDE8+UZBJrRd',
  'trusted_domains' =>
  array (
    0 => 'localhost',
  ),
  'datadirectory' => '/var/lib/nextcloud',
  'dbtype' => 'pgsql',
  'version' => '${version}',
  'overwrite.cli.url' => 'http://localhost',
  'dbname' => 'nextcloud',
  'dbhost' => 'localhost',
  'dbport' => '',
  'dbtableprefix' => 'oc_',
  'dbuser' => 'nextcloud',
  'dbpassword' => '${db_password}',
  'installed' => true,
% endif
);
