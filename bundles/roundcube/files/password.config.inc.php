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
$config['password_algorithm'] = 'dovecot';
$config['password_dovecotpw'] = '/usr/bin/sudo /usr/bin/doveadm pw';
$config['password_dovecotpw_method'] = 'ARGON2ID';
$config['password_dovecotpw_with_method'] = true;
$config['password_db_dsn'] = 'pgsql://mailserver:${mailserver_db_password}@localhost/mailserver';
$config['password_query'] = "UPDATE users SET password=%D FROM domains WHERE domains.id = domain_id AND domains.name = %d AND users.name = %l";
