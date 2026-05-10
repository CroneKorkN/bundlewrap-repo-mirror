# Managed by ckn-bw bundles/left4me. Local edits will be reverted.
DATABASE_URL=sqlite:////var/lib/left4me/left4me.db
SECRET_KEY=${node.metadata.get('left4me/secret_key')}
JOB_WORKER_THREADS=${node.metadata.get('left4me/job_worker_threads')}
SESSION_COOKIE_SECURE=true
