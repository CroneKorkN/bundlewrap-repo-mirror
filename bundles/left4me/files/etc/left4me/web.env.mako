# Managed by ckn-bw bundles/left4me. Local edits will be reverted.
DATABASE_URL=sqlite:////var/lib/left4me/left4me.db
SECRET_KEY=${node.metadata.get('left4me/secret_key')}
JOB_WORKER_THREADS=${node.metadata.get('left4me/job_worker_threads')}
SESSION_COOKIE_SECURE=true
LEFT4ME_PORT_RANGE_START=${node.metadata.get('left4me/port_range_start')}
LEFT4ME_PORT_RANGE_END=${node.metadata.get('left4me/port_range_end')}
STEAM_WEB_API_KEY=${node.metadata.get('left4me/steam_web_api_key')}
