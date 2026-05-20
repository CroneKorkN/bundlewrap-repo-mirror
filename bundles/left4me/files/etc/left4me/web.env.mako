# Managed by ckn-bw bundles/left4me. Local edits will be reverted.
DATABASE_URL=sqlite:////var/lib/left4me/left4me.db
SECRET_KEY=${node.metadata.get('left4me/secret_key')}
JOB_WORKER_THREADS=${node.metadata.get('left4me/job_worker_threads')}
SESSION_COOKIE_SECURE=true
LEFT4ME_PORT_RANGE_START=${node.metadata.get('left4me/port_range_start')}
LEFT4ME_PORT_RANGE_END=${node.metadata.get('left4me/port_range_end')}
STEAM_WEB_API_KEY=${node.metadata.get('left4me/steam_web_api_key')}
# Log listener destination — MUST be non-loopback because Source silently
# drops logaddress destinations in 127.0.0.0/8. Derived from the node's
# external IPv4; kernel routes same-host traffic via lo internally but the
# destination IP in the packet header must not literally be 127.x.
LOG_LISTENER_ADDR=${node.metadata.get('network/external/ipv4').split('/')[0]}:28000
LOG_LISTENER_BIND=0.0.0.0:28000
