from subprocess import check_output


def test_node(repo, node, **kwargs):
    for node in repo.nodes_in_group('mailserver'):
        domain = node.metadata.get('mailserver/hostname')
        expected_ptr_record = f"{domain}."
        expected_a_record = node.hostname

        # check A record
        actual_a_record = check_output(['dig', '+short', 'A', domain, '@9.9.9.9'], text=True).strip()
        if actual_a_record != expected_a_record:
            raise AssertionError(f"A record for {expected_a_record} on node {node.name} is {actual_a_record}, expected {expected_a_record}")

        # check otr record
        actual_ptr_record = check_output(['dig', '+short', '-x', expected_a_record, '@9.9.9.9'], text=True).strip()
        if actual_ptr_record != expected_ptr_record:
            raise AssertionError(f"PTR record for {expected_a_record} on node {node.name} is {actual_ptr_record}, expected {expected_ptr_record}")
