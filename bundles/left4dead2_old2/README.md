# https://github.com/SirPlease/L4D2-Competitive-Rework/blob/master/Dedicated%20Server%20Install%20Guide/README.md

getent passwd steam >/dev/null || useradd -M -d /opt/l4d2 -s /bin/bash steam
mkdir -p /opt/l4d2 /tmp/dumps
chown steam:steam /opt/l4d2 /tmp/dumps
dpkg --add-architecture i386
apt update
DEBIAN_FRONTEND=noninteractive apt install -y libc6:i386 lib32z1

function steam() { sudo -Hiu steam $* }

# -- STEAM -- #

steam mkdir -p /opt/l4d2/steam
test -f /opt/l4d2/steam/steamcmd_linux.tar.gz || \
  steam wget http://media.steampowered.com/installer/steamcmd_linux.tar.gz -P /opt/l4d2/steam
test -f /opt/l4d2/steam/steamcmd.sh || \
  steam tar -xvzf /opt/l4d2/steam/steamcmd_linux.tar.gz -C /opt/l4d2/steam

# fix: /opt/l4d2/.steam/sdk32/steamclient.so: cannot open shared object file: No such file or directory
steam mkdir -p /opt/l4d2/steam/.steam
test -f /opt/l4d2/steam/.steam/sdk32/steamclient.so || \
  steam ln -s /opt/l4d2/steam/linux32 /opt/l4d2/steam/.steam/sdk32

# -- INSTALL -- #

# erst die windows deps zu installieren scheint ein workaround für x64 zu sein?
steam mkdir -p /opt/l4d2/installation
steam /opt/l4d2/steam/steamcmd.sh \
    +force_install_dir /opt/l4d2/installation \
    +login anonymous \
    +@sSteamCmdForcePlatformType windows \
    +app_update 222860 validate \
    +quit
steam /opt/l4d2/steam/steamcmd.sh \
    +force_install_dir /opt/l4d2/installation \
    +login anonymous \
    +@sSteamCmdForcePlatformType linux \
    +app_update 222860 validate \
    +quit

# -- OVERLAYS -- #

steam mkdir -p /opt/l4d2/overlays

# workshop downloader
steam wget -4 https://git.sublimity.de/cronekorkn/steam-workshop-downloader/raw/branch/master/steam-workshop-download -P /opt/l4d2
steam chmod +x /opt/l4d2/steam-workshop-download

# -- OVERLAY PVE -- #

steam mkdir -p /opt/l4d2/overlays/pve

# admin system
steam mkdir -p /opt/l4d2/overlays/pve/left4dead2/addons
steam /opt/l4d2/steam-workshop-download 2524204971 --out /opt/l4d2/overlays/pve/left4dead2/addons
steam mkdir -p "/opt/l4d2/overlays/pve/left4dead2/ems/admin system"
echo "STEAM_1:0:12376499" | steam tee "/opt/l4d2/overlays/pve/left4dead2/ems/admin system/admins.txt"

# ions vocalizer
steam /opt/l4d2/steam-workshop-download 698857882 --out /opt/l4d2/overlays/pve/left4dead2/addons

# -- OVERLAY ZONEMOD -- #

true

# -- SERVERS -- #

steam mkdir -p /opt/l4d2/servers

# -- SERVER PVE1 -- #

steam mkdir -p \
  /opt/l4d2/servers/pve1 \
  /opt/l4d2/servers/pve1/work \
  /opt/l4d2/servers/pve1/upper \
  /opt/l4d2/servers/pve1/merged

mount -t overlay overlay \
  -o lowerdir=/opt/l4d2/overlays/pve:/opt/l4d2/installation,upperdir=/opt/l4d2/servers/pve1/upper,workdir=/opt/l4d2/servers/pve1/work \
  /opt/l4d2/servers/pve1/merged

# run server
steam cat <<'EOF' > /opt/l4d2/servers/pve1/merged/left4dead2/cfg/server.cfg
hostname "CKNs Server"
motd_enabled 0

sv_steamgroup "38347879"
#sv_steamgroup_exclusive 0

sv_minrate 60000
sv_maxrate 0
net_splitpacket_maxrate 60000

sv_hibernate_when_empty 0
EOF
steam /opt/l4d2/servers/pve1/merged/srcds_run -game left4dead2 -ip 0.0.0.0 -port 27015 +map c1m1_hotel
