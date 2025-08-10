from shlex import quote


def steam_run(cmd):
    return f'su - steam -c {quote(cmd)}'


users = {
    'steam': {
        'home': '/opt/steam',
    },
}

directories = {
    '/opt/steam': {
        'owner': 'steam',
        'group': 'steam',
    },
    '/opt/steam/.steam': {
        'owner': 'steam',
        'group': 'steam',
    },
    '/opt/left4dead2': {
        'owner': 'steam',
        'group': 'steam',
    },
    '/opt/left4dead2/left4dead2/ems/admin system': {
        'owner': 'steam',
        'group': 'steam',
    },
    '/opt/left4dead2/left4dead2/addons': {
        'owner': 'steam',
        'group': 'steam',
    },
    '/tmp/dumps': {
        'owner': 'steam',
        'group': 'steam',
        'mode': '1770',
    },
}

symlinks = {
    '/opt/steam/.steam/sdk32': {
        'target': '/opt/steam/linux32',
        'owner': 'steam',
        'group': 'steam',
    },
}

files = {
    '/opt/steam-workshop-download': {
        'content_type': 'download',
        'source': 'https://git.sublimity.de/cronekorkn/steam-workshop-downloader/raw/branch/master/steam-workshop-download',
        'mode': '755',
    },
    '/opt/left4dead2/left4dead2/ems/admin system/admins.txt': {
        'unless': 'test -f /opt/left4dead2/left4dead2/ems/admin system/admins.txt',
        'content': 'STEAM_1:0:12376499',
        'owner': 'steam',
        'group': 'steam',
    },
}

actions = {
    'dpkg_add_architecture': {
        'command': 'dpkg --add-architecture i386',
        'unless': 'dpkg --print-foreign-architectures | grep -q i386',
        'triggers': [
            'action:apt_update',
        ],
        'needed_by': [
            'pkg_apt:libc6_i386',
        ],
    },
    'download_steam': {
        'command': steam_run('wget http://media.steampowered.com/installer/steamcmd_linux.tar.gz -P /opt/steam'),
        'unless':  steam_run('test -f /opt/steam/steamcmd_linux.tar.gz'),
        'needs': {
            'pkg_apt:libc6_i386',
            'directory:/opt/steam',
        }
    },
    'extract_steamcmd': {
        'command': steam_run('tar -xvzf /opt/steam/steamcmd_linux.tar.gz -C /opt/steam'),
        'unless': steam_run('test -f /opt/steam/steamcmd.sh'),
        'needs': {
            'action:download_steam',
        }
    },
}

for addon_id in [2524204971]:
    actions[f'download-left4dead2-addon-{addon_id}'] = {
        'command': steam_run(f'/opt/steam-workshop-download {addon_id} --out /opt/left4dead2/left4dead2/addons'),
        'unless': steam_run(f'test -f /opt/left4dead2/left4dead2/addons/{addon_id}.vpk'),
        'needs': {
            'directory:/opt/left4dead2/left4dead2/addons',
        },
        'needed_by': {
            'tag:left4dead2-servers',
        },
    }

svc_systemd = {
    'left4dead2-install.service': {
        'enabled': True,
        'running': False,
        'needs': {
            'file:/usr/local/lib/systemd/system/left4dead2-install.service',
        },
    },
}

for server_name, server_config in node.metadata.get('left4dead2/servers', {}).items():
    svc_systemd[f'left4dead2-{server_name}.service'] = {
        'enabled': True,
        'running': True,
        'tags': {
            'left4dead2-servers',
        },
        'needs': {
            'svc_systemd:left4dead2-install.service',
            f'file:/usr/local/lib/systemd/system/left4dead2-{server_name}.service',
        }
    }



# # https://github.com/SirPlease/L4D2-Competitive-Rework/blob/master/Dedicated%20Server%20Install%20Guide/README.md

# mkdir /opt/steam /tmp/dumps
# useradd -M -d /opt/steam -s /bin/bash steam
# chown steam:steam /opt/steam /tmp/dumps
# dpkg --add-architecture i386
# apt update
# apt install libc6:i386 lib32z1
# sudo su - steam -s /bin/bash

# #--------

# wget http://media.steampowered.com/installer/steamcmd_linux.tar.gz
# tar -xvzf steamcmd_linux.tar.gz

# # fix: /opt/steam/.steam/sdk32/steamclient.so: cannot open shared object file: No such file or directory
# mkdir /opt/steam/.steam && ln -s /opt/steam/linux32 /opt/steam/.steam/sdk32

# # erst die windows deps zu installieren scheint ein workaround für x64 zu sein?
# ./steamcmd.sh \
#     +force_install_dir /opt/steam/left4dead2 \
#     +login anonymous \
#     +@sSteamCmdForcePlatformType windows \
#     +app_update 222860 validate \
#     +quit
# ./steamcmd.sh \
#     +force_install_dir /opt/steam/left4dead2 \
#     +login anonymous \
#     +@sSteamCmdForcePlatformType linux \
#     +app_update 222860 validate \
#     +quit

# # download admin system
# wget -4 https://git.sublimity.de/cronekorkn/steam-workshop-downloader/raw/branch/master/steam-workshop-download
# chmod +x steam-workshop-download
# ./steam-workshop-download 2524204971 --out /opt/steam/left4dead2/left4dead2/addons
# mkdir -p "/opt/steam/left4dead2/left4dead2/ems/admin system"
# echo "STEAM_1:0:12376499" > "/opt/steam/left4dead2/left4dead2/ems/admin system/admins.txt"

# /opt/steam/left4dead2/srcds_run -game left4dead2 -ip 0.0.0.0 -port 27015 +map c1m1_hotel


# cat <<'EOF' > /opt/steam/left4dead2/left4dead2/cfg/server.cfg
# hostname "CKNs Server"
# motd_enabled 0

# sv_steamgroup "38347879"
# #sv_steamgroup_exclusive 0

# sv_minrate 60000
# sv_maxrate 0
# net_splitpacket_maxrate 60000

# sv_hibernate_when_empty 0
# EOF
