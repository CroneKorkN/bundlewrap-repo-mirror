<?php
# https://docs.nextcloud.com/server/stable/admin_manual/configuration_server/config_sample_php_parameters.html#multiple-config-php-file
$CONFIG = json_decode(file_get_contents("/etc/nextcloud/managed.config.json"), $associative = true);
