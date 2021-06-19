from os.path import join

service_account = node.metadata.get('gcloud/service_account')
project = node.metadata.get('gcloud/project')

files[f'/root/.config/gcloud/service_account.json'] = {
    'content': repo.vault.decrypt_file(
        join(repo.path, 'data', 'gcloud', 'service_accounts', f'{service_account}@{project}.json.enc')
    ),
    'mode': '500',
    'needs': [
        'pkg_apt:google-cloud-sdk',
    ],
}

actions['gcloud_activate_service_account'] = {
    'command': 'gcloud auth activate-service-account --key-file /root/.config/gcloud/service_account.json',
    'unless': f"gcloud auth list | grep -q '^\*[[:space:]]*{service_account}@{project}.iam.gserviceaccount.com'",
    'needs': [
        f'file:/root/.config/gcloud/service_account.json'
    ],
}

actions['gcloud_select_project'] = {
    'command': f"gcloud config set project '{project}'",
    'unless': f"gcloud config get-value project | grep -q '^{project}$'",
    'needs': [
        f'action:gcloud_activate_service_account'
    ],
}
