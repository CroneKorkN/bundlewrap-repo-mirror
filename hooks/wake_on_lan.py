"""wake_on_lan: pre-apply / pre-run hook that wakes a node via libs.wol before bw connects to it."""


def wake_on_lan(node):
    node.repo.libs.wol.wake(node)

def node_apply_start(repo, node, **kwargs):
    wake_on_lan(node)

def node_run_start(repo, node, cmd, **kwargs):
    wake_on_lan(node)
