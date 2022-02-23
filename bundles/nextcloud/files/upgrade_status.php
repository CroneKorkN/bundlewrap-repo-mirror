<?php

require_once '/opt/nextcloud/lib/base.php';

if (\OCP\Util::needUpgrade()) {
    exit(99);
} else {
    exit(0);
}
