"""test_ptr_records: bw-test gate verifying live A/PTR DNS records for the `mailserver` group via DNS-over-HTTPS."""

import json
from ipaddress import ip_address
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# DNS-over-HTTPS instead of dig: the agent sandbox allows no UDP, only HTTPS through its proxy
DOH_URL = 'https://dns.google/resolve'
DOH_TIMEOUT = 10


def resolve(name, rtype):
    query = urlencode({'name': name, 'type': rtype})
    with urlopen(Request(f'{DOH_URL}?{query}', headers={'accept': 'application/dns-json'}), timeout=DOH_TIMEOUT) as response:
        answer = json.load(response)
    if answer.get('Status') != 0:
        raise AssertionError(f"{rtype} lookup for {name} failed with DNS status {answer.get('Status')}")
    return [record['data'] for record in answer.get('Answer', []) if record['type'] == {'A': 1, 'PTR': 12}[rtype]]


def test(repo, **kwargs):
    for node in repo.nodes_in_group('mailserver'):
        domain = node.metadata.get('mailserver/hostname')
        expected_ptr_record = f"{domain}."
        expected_a_record = node.hostname

        # check A record
        actual_a_records = resolve(domain, 'A')
        if actual_a_records != [expected_a_record]:
            raise AssertionError(f"A record for {domain} on node {node.name} is {actual_a_records}, expected {expected_a_record}")

        # check PTR record
        actual_ptr_records = resolve(ip_address(expected_a_record).reverse_pointer, 'PTR')
        if actual_ptr_records != [expected_ptr_record]:
            raise AssertionError(f"PTR record for {expected_a_record} on node {node.name} is {actual_ptr_records}, expected {expected_ptr_record}")
