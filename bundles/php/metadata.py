defaults = {
}


@metadata_reactor.provides(
    'php/php.ini',
)
def php_ini(metadata):
    conf = {
        'PHP': {
            'engine': 'On',
            'short_open_tag': 'Off',
            'precision': '14',
            'output_buffering': '4096',
            'zlib.output_compression': 'Off',
            'implicit_flush': 'Off',
            'serialize_precision': '-1',
            'ignore_user_abort': 'Off',
            'zend.enable_gc': 'On',
            'expose_php': 'Off',
            'max_execution_time': '300',
            'max_input_time': '600',
            'memory_limit': '512M',
            'error_reporting': '"E_ALL & ~E_DEPRECATED & ~E_STRICT"',
            'display_startup_errors': 'Off',
            'log_errors': 'On',
            'log_errors_max_len': '1024',
            'ignore_repeated_errors': 'Off',
            'ignore_repeated_source': 'Off',
            'report_memleaks': 'On',
            'html_errors': 'On',
            'error_log': 'syslog',
            'syslog.ident': 'php',
            'syslog.filter': 'ascii',
            'arg_separator.output': '"&amp;"',
            'variables_order': 'GPCS',
            'request_order': 'GP',
            'register_argc_argv': 'Off',
            'auto_globals_jit': 'On',
            'post_max_size': '32g',
            'default_mimetype': 'text/html',
            'default_charset': 'UTF-8',
            'enable_dl': 'Off',
            'file_uploads': 'On',
            'upload_max_filesize': '32g',
            'max_file_uploads': '2000',
            'allow_url_fopen': 'On',
            'allow_url_include': 'Off',
            'default_socket_timeout': '10',
        },
        'CLI Server': {
            'cli_server.color': 'On',
        },
        'mail function': {
            'mail.add_x_header': 'Off',
        },
        'ODBC': {
            'odbc.allow_persistent': 'On',
            'odbc.check_persistent': 'On',
            'odbc.max_persistent': '-1',
            'odbc.max_links': '-1',
            'odbc.defaultlrl': '4096',
            'odbc.defaultbinmode': '1',
        },
        'PostgreSQL': {
            'pgsql.allow_persistent': 'On',
            'pgsql.auto_reset_persistent': 'Off',
            'pgsql.max_persistent': '-1',
            'pgsql.max_links': '-1',
            'pgsql.ignore_notice': '0',
            'pgsql.log_notice': '0',
        },
        'bcmath': {
            'bcmath.scale': '0',
        },
        'Session': {
            'session.save_handler': 'files',
            'session.use_strict_mode': '0',
            'session.use_cookies': '1',
            'session.use_only_cookies': '1',
            'session.name': 'PHPSESSID',
            'session.auto_start': '0',
            'session.cookie_lifetime': '0',
            'session.cookie_path': '/',
            'session.cookie_domain': '',
            'session.cookie_httponly': '',
            'session.cookie_samesite': '',
            'session.serialize_handler': 'php',
            'session.gc_probability': '1',
            'session.gc_divisor': '1000',
            'session.gc_maxlifetime': '1440',
            'session.referer_check': '',
            'session.cache_limiter': 'nocache',
            'session.cache_expire': '180',
            'session.use_trans_sid': '0',
            'session.sid_length': '32',
            'session.trans_sid_tags': '"a=href,area=href,frame=src,form="',
            'session.sid_bits_per_character': '6',
        },
        'Assertion': {
            'zend.assertions': '-1',
        },
        'Date': {
            'date.timezone': 'Europe/London',
        },
        'opcache': {
            'opcache.enable': '1',
            'opcache.interned_strings_buffer': '32',
            'opcache.max_accelerated_files': '20000',
            'opcache.memory_consumption': '1024',
            'opcache.save_comments': '1',
            'opcache.validate_timestamps': '1',
            'opcache.revalidate_freq': '60',
        },
    }
    
    return {
        'php': {
            'php.ini': {
                section: {
                    key: value
                        for key, value in options.items()
                        if not metadata.get(f'php/php.ini/{section}/{key}', None)
                }
                    for section, options in conf.items()
            }
        },
    }


@metadata_reactor.provides(
    'php/www.conf',
)
def www_conf(metadata):
    return {
        'php': {
            'www.conf': {
                'user': 'www-data',
                'group': 'www-data',
                'listen': f"/run/php/php{metadata.get('php/version')}-fpm.sock",
                'listen.owner': 'www-data',
                'listen.group': 'www-data',
                'pm': 'dynamic',
                'pm.max_children': '30',
                'pm.start_servers': '10',
                'pm.min_spare_servers': '5',
                'pm.max_spare_servers': '10',
                'pm.max_requests': '500',
            },
        },
    }


@metadata_reactor.provides(
    'apt/packages',
)
def apt(metadata):
    return {
        'apt': {
            'packages': {
                f"php{metadata.get('php/version')}": {},
                f"php{metadata.get('php/version')}-fpm": {},
            },
        },
    }
