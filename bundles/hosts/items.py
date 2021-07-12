from ipaddress import ip_address
from collections import OrderedDict

def sorted_hostnames(hostnames):
    return sorted(
        hostnames,
        key=lambda e: (len(e.split('.')), e),
    )

def sorted_hosts_for_ip_version(version):
    return OrderedDict(
        sorted(
            [
                (ip, sorted_hostnames(hostnames))
                    for ip, hostnames in node.metadata.get('hosts').items()
                    if ip_address(ip).version == version
            ],
            key=lambda e: ip_address(e[0]),
        ),
    )


sorted_hosts = OrderedDict({
    **sorted_hosts_for_ip_version(4),
    **sorted_hosts_for_ip_version(6),
})
ip_width = len(max(sorted_hosts.keys(), key=len))

files['/etc/hosts'] = {
    'content': '\n'.join(
        ' '.join([
            ip.ljust(ip_width, ' '),
            *hostnames
        ])
            for ip, hostnames in sorted_hosts.items()
    ),
}

    
