from bundlewrap.operations import run_local
from bundlewrap.utils.ui import io
from bundlewrap.utils.text import yellow, bold


def node_apply_start(repo, node, interactive=False, **kwargs):
    if node.has_bundle('wol-sleeper'):
        io.stdout('{x} {node}  waking up...'.format(
            x=yellow('!'),
            node=bold(node.name)
        ))
        repo\
            .get_node(node.metadata.get('wol-sleeper/waker'))\
            .run(node.metadata.get('wol-sleeper/wake_command'))
