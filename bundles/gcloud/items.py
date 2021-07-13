from os.path import join
from json import dumps

service_account = node.metadata.get('gcloud/service_account')
project = node.metadata.get('gcloud/project')

directories[f'/etc/gcloud'] = {
    'purge': True,
}

files['/etc/gcloud/gcloud.json'] = {
    'content': dumps(
        node.metadata.get('gcloud'),
        indent=4,
        sort_keys=True
    ),
}

files['/etc/gcloud/service_account.json'] = {
    'content': repo.vault.decrypt_file(
        join(repo.path, 'data', 'gcloud', 'service_accounts', f'{service_account}@{project}.json.enc')
    ),
    'mode': '500',
    'needs': {
        'pkg_apt:google-cloud-sdk',
    },
}

actions['gcloud_activate_service_account'] = {
    'command': 'gcloud auth activate-service-account --key-file /etc/gcloud/service_account.json',
    'unless': f"gcloud auth list | grep -q '^\*[[:space:]]*{service_account}@{project}.iam.gserviceaccount.com'",
    'needs': {
        f'file:/etc/gcloud/service_account.json'
    },
}

actions['gcloud_select_project'] = {
    'command': f"gcloud config set project '{project}'",
    'unless': f"gcloud config get-value project | grep -q '^{project}$'",
    'needs': {
        f'action:gcloud_activate_service_account'
    },
}
