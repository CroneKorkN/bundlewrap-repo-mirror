<?php

% if installer:
$config['enable_installer'] = true;
% endif

/* Local configuration for Roundcube Webmail */

$config['db_dsnw'] = '${database['provider']}://${database['user']}:${database['password']}@${database['host']}/${database['name']}';
$config['imap_host'] = 'localhost';
$config['smtp_host'] = 'tls://localhost';
$config['smtp_user'] = '%u';
$config['smtp_pass'] = '%p';
$config['support_url'] = '';
$config['des_key'] = '${des_key}';
$config['product_name'] = '${product_name}';
$config['plugins'] = array(${', '.join(f'"{plugin}"' for plugin in plugins)});
$config['language'] = 'de_DE';
$config['smtp_conn_options'] = array(
   'ssl' => array(
   'verify_peer' => false,
   'verify_peer_name' => false,
  ),
);
