# https://github.com/freescout-helpdesk/freescout/wiki/Installation-Guide

directories = {
    '/opt/freescout': {
        'owner': 'www-data',
        'group': 'www-data',
        # chown -R www-data:www-data /opt/freescout
    },
}

git_deploy = {
    '/opt/freescout': {
        'repo': 'https://github.com/freescout-helpdesk/freescout.git',
        'rev': 'master',
    },
}


files = {
}
