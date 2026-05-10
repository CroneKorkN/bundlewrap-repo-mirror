"""skip_local_nodes: skip apply on `localhost` nodes whose metadata `id` doesn't match this host's local_id."""

from bundlewrap.exceptions import SkipNode

def node_apply_start(repo, node, interactive, **kwargs):
    if node.hostname == 'localhost':
        if node.metadata.get('id') != repo.libs.local.id():
            raise SkipNode('bw is not currently running on this node')
