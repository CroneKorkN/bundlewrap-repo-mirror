<?php

% if installer:
$config['enable_installer'] = true;
% endif

/* Local configuration for Roundcube Webmail */

$config['db_dsnw'] = '${database['provider']}://${database['user']}:${database['password']}@${database['host']}/${database['name']}';
# without tls: the name resolves to the server's own ip, which dovecot treats as secure like localhost;
# keep the name, roundcube keys its users by it
$config['imap_host'] = '${imap_host}:143';
# php's default_socket_timeout is 10s, moving many messages takes longer
$config['imap_timeout'] = 120;
# folder lists, sort orders and message structures in the roundcube db, synced via condstore/qresync
$config['imap_cache'] = 'db';
$config['messages_cache'] = true;
#$config['imap_debug'] = true;
$config['smtp_host'] = 'tls://${imap_host}';
$config['smtp_port'] = 587;
$config['smtp_user'] = '%u';
$config['smtp_pass'] = '%p';
#$config['smtp_debug'] = true;
$config['support_url'] = '';
$config['des_key'] = '${des_key}';
$config['product_name'] = '${product_name}';
$config['plugins'] = array(${', '.join(f'"{plugin}"' for plugin in plugins)});
$config['language'] = 'de_DE';
