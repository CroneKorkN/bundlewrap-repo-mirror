def test_unique_node_ids(repo):
    ids = {}
    for node in repo.nodes:
        if node.metadata.get('id') in ids:
            raise ValueError(f"Duplicate node ID found: {node.metadata.get('id')} in node {node.name} and {ids[node.metadata.get('id')]}")
        ids[node.metadata.get('id')] = node.name


def apply_start(repo, target, nodes, interactive=False, **kwargs):
    test_unique_node_ids(repo)


def test(repo, **kwargs):
    test_unique_node_ids(repo)
