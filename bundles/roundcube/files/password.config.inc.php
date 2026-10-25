<?php

$config['password_driver'] = 'sql';
$config['password_strength_driver'] = null;
$config['password_confirm_current'] = true;
$config['password_minimum_length'] = 8;
$config['password_minimum_score'] = 0;
$config['password_log'] = true;
$config['password_hosts'] = null;
$config['password_force_save'] = false;
$config['password_force_new_user'] = false;
$config['password_algorithm'] = 'hash-argon2id';
$config['password_algorithm_prefix'] = true;
# owasp minimum: dovecot verifies it on every imap login, doveadm pw's 64 MiB and 3 passes take 250 ms there
$config['password_algorithm_options'] = ['memory_cost' => 19456, 'time_cost' => 2, 'threads' => 1];
$config['password_db_dsn'] = 'pgsql://mailserver:${mailserver_db_password}@localhost/mailserver';
$config['password_query'] = "UPDATE users SET password = %P FROM domains WHERE domains.id = users.domain_id AND domains.name = %d AND users.name = %l";
