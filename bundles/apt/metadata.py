defaults = {
    'apt': {
        'packages': {
            'apt-listchanges': {
                'installed': False,
            },
            'ca-certificates': {},
        },
        'config': {
            'DPkg': {
                'Pre-Install-Pkgs': {
                    '/usr/sbin/dpkg-preconfigure --apt || true',
                },
                'Post-Invoke': {
                    # keep package cache empty
                    '/bin/rm -f /var/cache/apt/archives/*.deb || true',
                },
                'Options': {
                    # https://unix.stackexchange.com/a/642541/357916
                    '--force-confold',
                    '--force-confdef',
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
                'Move-Autobit-Sections': {
                    'oldlibs',
                },
                'Update': {
                    # https://unix.stackexchange.com/a/653377/357916
                    'Error-Mode': 'any',
                },
            },
        },
        'sources': {},
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
    'apt/sources',
)
def key(metadata):
    return {
        'apt': {
            'sources': {
                source_name: {
                    'key': source_name,
                }
                    for source_name, source_config in metadata.get('apt/sources').items()
                    if 'key' not in source_config
            },
        },
    }


@metadata_reactor.provides(
    'apt/sources',
)
def signed_by(metadata):
    return {
        'apt': {
            'sources': {
                source_name: {
                    'options': {
                        'Signed-By': '/etc/apt/keyrings/' + metadata.get(f'apt/sources/{source_name}/key') + '.' + repo.libs.apt.find_keyfile_extension(node, metadata.get(f'apt/sources/{source_name}/key')),
                    },
                }
                    for source_name in metadata.get('apt/sources')
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


# @metadata_reactor.provides(
#     'apt/config',
#     'apt/list_changes',
# )
# def listchanges(metadata):
#     return {
#         'apt': {
#             'config': {
#                 'DPkg': {
#                     'Pre-Install-Pkgs': {
#                         '/usr/bin/apt-listchanges --apt || test $? -lt 10',
#                     },
#                     'Tools': {
#                         'Options': {
#                             '/usr/bin/apt-listchanges': {
#                                 'Version': '2',
#                                 'InfoFD': '20',
#                             },
#                         },
#                     },
#                 },
#                 'Dir': {
#                     'Etc': {
#                         'apt-listchanges-main': 'listchanges.conf',
#                         'apt-listchanges-parts': 'listchanges.conf.d',
#                     },
#                 },
#             },
#             'list_changes': {
#                 'apt': {
#                     'frontend': 'pager',
#                     'which': 'news',
#                     'email_address': 'root',
#                     'email_format': 'text',
#                     'confirm': 'false',
#                     'headers': 'false',
#                     'reverse': 'false',
#                     'save_seen': '/var/lib/apt/listchanges.db',
#                 },
#             },
#         },
#     }
