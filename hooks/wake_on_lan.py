from bundlewrap.operations import run_local

def node_apply_start(repo, node, interactive=False, **kwargs):
    if node.has_bundle('wol-sleeper'):
        repo\
            .get_node(node.metadata.get('wol-sleeper/waker'))\
            .run(node.metadata.get('wol-sleeper/wake_command'))
