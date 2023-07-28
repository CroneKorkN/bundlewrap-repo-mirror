from os.path import expanduser


def apply_start(repo, target, nodes, interactive=False, **kwargs):
    with open(expanduser('~/.ssh/known_hosts_ckn'), 'w+') as file:
        file.write('\n'.join(sorted(
            repo.libs.ssh.known_hosts_entry_for(node)
                for node in repo.nodes
                if node.has_bundle('ssh')
        )))
