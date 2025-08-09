# https://github.com/SirPlease/L4D2-Competitive-Rework/blob/master/Dedicated%20Server%20Install%20Guide/README.md

mkdir /opt/steam /tmp/dumps
useradd -M -d /opt/steam -s /bin/bash steam
chown steam:steam /opt/steam /tmp/dumps
dpkg --add-architecture i386
apt update
apt install libc6:i386 lib32z1
sudo su - steam -s /bin/bash

#--------

wget http://media.steampowered.com/installer/steamcmd_linux.tar.gz
tar -xvzf steamcmd_linux.tar.gz

# erst die windows deps zu installieren scheint ein workaround für x64 zu sein?
./steamcmd.sh \
    +force_install_dir /opt/steam/left4dead2 \
    +login anonymous \
    +@sSteamCmdForcePlatformType windows \
    +app_update 222860 validate \
    +quit
./steamcmd.sh \
    +force_install_dir /opt/steam/left4dead2 \
    +login anonymous \
    +@sSteamCmdForcePlatformType linux \
    +app_update 222860 validate \
    +quit

# fix: /opt/steam/.steam/sdk32/steamclient.so: cannot open shared object file: No such file or directory
mkdir /opt/steam/.steam && ln -s /opt/steam/linux32 /opt/steam/.steam/sdk32

# download admin system
wget -4 https://git.sublimity.de/cronekorkn/steam-workshop-downloader/raw/branch/master/steam-workshop-download
chmod +x steam-workshop-download
./steam-workshop-download 2524204971 --out /opt/steam/left4dead2/left4dead2/addons
mkdir -p "/opt/steam/left4dead2/left4dead2/ems/admin system"
echo "STEAM_1:0:12376499" > "/opt/steam/left4dead2/left4dead2/ems/admin system/admins.txt"

/opt/steam/left4dead2/srcds_run -game left4dead2 -ip 0.0.0.0 -port 27015 +map c1m1_hotel


# /opt/steam/left4dead2/left4dead2/cfg/server.cfg
hostname "CKNs Server"
motd_enabled 0

sv_minrate 60000
sv_maxrate 0
net_splitpacket_maxrate 60000

sv_steamgroup "38347879"
sv_steamgroup_exclusive 1