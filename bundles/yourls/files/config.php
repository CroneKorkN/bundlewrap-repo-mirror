<?php
define( 'YOURLS_DB_USER', 'yourls' );
define( 'YOURLS_DB_PASS', '${db_password}' );
define( 'YOURLS_DB_NAME', 'yourls' );
define( 'YOURLS_DB_HOST', 'localhost' );
define( 'YOURLS_DB_PREFIX', 'yourls_' );

define( 'YOURLS_SITE', 'https://${hostname}' );
define( 'YOURLS_LANG', '' );
define( 'YOURLS_UNIQUE_URLS', true );
define( 'YOURLS_PRIVATE', true );
define( 'YOURLS_COOKIEKEY', '${cookiekey}' );

$yourls_user_passwords = [
% for username, password in users.items():
	'${username}' => '${password}',
% endfor
];

define( 'YOURLS_URL_CONVERT', 36 );

define( 'YOURLS_DEBUG', false );

$yourls_reserved_URL = [];