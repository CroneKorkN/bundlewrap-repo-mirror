# state
smartctl -n idle /dev/sda

# temp
smartctl -n idle -A /dev/sdb --json=c | jq .temperature.current

# apm
smartctl --get apm /dev/sdb --json=c | jq .ata_apm.level
smartctl --set apm,20 /dev/sdb --json=c

# power state
smartctl -n idle /dev/sdb

# devices
smartctl --scan | cut -d' ' -f1
