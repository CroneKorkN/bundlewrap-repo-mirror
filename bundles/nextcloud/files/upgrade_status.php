<?php

require_once __DIR__ . '/lib/base.php';

if (\OCP\Util::needUpgrade()) {
    exit(99);
} else {
    exit(0);
}
