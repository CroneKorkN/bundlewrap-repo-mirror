def node_apply_start(repo, node, **kwargs):
    repo.libs.wol.wake(node)

def node_run_start(repo, node, cmd, **kwargs):
    repo.libs.wol.wake(node)
