<?php

% if installer:
$config['enable_installer'] = true;
% endif

/* Local configuration for Roundcube Webmail */

$config['db_dsnw'] = '${database['provider']}://${database['user']}:${database['password']}@${database['host']}/${database['name']}';
$config['imap_host'] = 'ssl://${imap_host}';
$config['imap_port'] = 993;
$config['smtp_host'] = 'tls://localhost';
$config['smtp_port'] = 587;
$config['smtp_user'] = '%u';
$config['smtp_pass'] = '%p';
#$config['imap_debug'] = true;
#$config['smtp_debug'] = true;
$config['support_url'] = '';
$config['des_key'] = '${des_key}';
$config['product_name'] = '${product_name}';
$config['plugins'] = array(${', '.join(f'"{plugin}"' for plugin in plugins)});
$config['language'] = 'de_DE';
