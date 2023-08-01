from os.path import expanduser


def apply_start(repo, target, nodes, interactive=False, **kwargs):
    with open(expanduser('~/.ssh/known_hosts_ckn'), 'w+') as file:
        file.write('\n'.join(sorted(
            line
                for node in repo.nodes
                if node.has_bundle('ssh')
                for line in node.metadata.get('ssh/is_known_as')

        )))
