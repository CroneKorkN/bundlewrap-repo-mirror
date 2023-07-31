defaults = {
    'apt': {
        'config': {
            'DPkg': {
                'Pre-Install-Pkgs': {
                    '/usr/sbin/dpkg-preconfigure --apt || true',
                },
                'Post-Invoke': {
                    '/bin/rm -f /var/cache/apt/archives/*.deb || true',
                },
            },
            'APT': {
                'NeverAutoRemove': {
                    '^firmware-linux.*',
                    '^linux-firmware$',
                    '^linux-image-[a-z0-9]*$',
                    '^linux-image-[a-z0-9]*-[a-z0-9]*$',
                },
                'VersionedKernelPackages': {
                    # kernels
                    'linux-.*',
                    'kfreebsd-.*',
                    'gnumach-.*',
                    # (out-of-tree) modules
                    '.*-modules',
                    '.*-kernel',
                },
                'Never-MarkAuto-Sections': {
                    'metapackages',
                    'tasks',
                },
                'Move-Autobit-Sections': 'oldlibs',
            },
        },
        'sources': set(),
    },
    'monitoring': {
        'services': {
            'apt upgradable': {
                'vars.command': '/usr/lib/nagios/plugins/check_apt_upgradable',
                'vars.sudo': True,
                'check_interval': '1h',
            },
            'current kernel': {
                'vars.command': 'ls /boot/vmlinuz-* | sort -V | tail -n 1 | xargs -n1 basename | cut -d "-" -f 2- | grep -q "^$(uname -r)$"',
                'check_interval': '1h',
            },
            'apt reboot-required': {
                'vars.command': 'ls /var/run/reboot-required 2> /dev/null && exit 1 || exit 0',
                'check_interval': '1h',
            },
        },
    },
}


@metadata_reactor.provides(
    'apt/config',
    'apt/packages',
)
def unattended_upgrades(metadata):
    return {
        'apt': {
            'config': {
                'APT': {
                    'Periodic': {
                        'Update-Package-Lists': '1',
                        'Unattended-Upgrade': '1',
                    },
                },
                'Unattended-Upgrade': {
                    'Origins-Pattern': {
                        "origin=*",
                    },
                },
            },
            'packages': {
                'unattended-upgrades': {},
            },
        },
    }


@metadata_reactor.provides(
    'apt/config',
    'apt/list_changes',
)
def listchanges(metadata):
    return {
        'apt': {
            'config': {
                'DPkg': {
                    'Pre-Install-Pkgs': {
                        '/usr/bin/apt-listchanges --apt || test $? -lt 10',
                    },
                },
                'Tools': {
                    'Options': {
                        '/usr/bin/apt-listchanges': {
                            'Version': '2',
                            'InfoFD': '20',
                        },
                    },
                },
                'Dir': {
                    'Etc': {
                        'apt-listchanges-main': 'listchanges.conf',
                        'apt-listchanges-parts': 'listchanges.conf.d',
                    },
                },
            },
            'list_changes': {
                'apt': {
                    'frontend': 'pager',
                    'which': 'news',
                    'email_address': 'root',
                    'email_format': 'text',
                    'confirm': 'false',
                    'headers': 'false',
                    'reverse': 'false',
                    'save_seen': '/var/lib/apt/listchanges.db',
                },
            },
        },
    }
