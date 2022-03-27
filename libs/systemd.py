from mako.template import Template

template = '''
% for segment, options in data.items():

%     if '#' in segment:
# ${segment.split('#', 2)[1]}
%     endif
[${segment.split('#')[0]}]
%     for option, value in options.items():
%         if isinstance(value, dict):
%             for k, v in value.items():
${option}=${k}=${v}
%             endfor
%         elif isinstance(value, (list, set, tuple)):
%             for item in sorted(value):
${option}=${item}
%             endfor
%         else:
${option}=${str(value)}
%         endif
%     endfor
% endfor
'''

order = [
    'Unit',
    'Timer',
    'Service',
    'Install',
]

def segment_order(segment):
    return (
        order.index(segment[0]) if segment[0] in order else float('inf'),
        segment[0]
    )

def generate_unitfile(data):
    return Template(template).render(
        data=dict(sorted(data.items(), key=segment_order)),
        order=order
    ).lstrip()

# wip
def protection():
    return {
        # user
        'UMask': '077',
        'DynamicUser': 'yes',
        'PrivateUsers': 'yes',
        'RestrictSUIDSGID': 'yes',
        'NoNewPrivileges': 'yes',
        'LockPersonality': 'yes',
        'RemoveIPC': 'yes',

        # fs
        'ProtectSystem': 'strict',
        'ProtectHome': 'yes',
        'PrivateTmp': 'yes',
        'PrivateDevices': 'yes',
        'ProtectProc': 'invisible',
        'ProcSubset': 'pid',
        'PrivateMounts': 'yes',
        'RestrictFileSystems': {'ext4', 'tmpfs', 'zfs'},

        'NoExecPaths': {'/'},
        'ExecPaths': {'/bin', '/sbin', '/lib', '/lib64', '/usr'},

        'TemporaryFileSystem': {'/var'},

        # network
        'IPAddressDeny': 'any',
        'PrivateNetwork': 'yes',
        'RestrictAddressFamilies': 'none',

        # syscall
        'SystemCallArchitectures': 'native',
        'SystemCallFilter': '~@swap @resources @reboot @raw-io @privileged @obsolete @mount @module @debug @cpu-emulation @clock',

        # else
        'ProtectHostname': 'yes',
        'ProtectClock': 'yes',
        'ProtectKernelTunables': 'yes',
        'ProtectKernelModules': 'yes',
        'ProtectKernelLogs': 'yes',
        'ProtectControlGroups': 'yes',
        'RestrictNamespaces': 'yes',
        'MemoryDenyWriteExecute': 'yes',
        'RestrictRealtime': 'yes',
        'CapabilityBoundingSet': '',
    }
