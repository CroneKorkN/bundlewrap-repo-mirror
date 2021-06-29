# setup

- apply influxdb to server
- write client_token into influxdb metadata:
  `influx auth list --json | jq -r '.[] | select (.description == "client_token") | .token'`
- apply clients

# reset password

Opening /var/lib/influxdb/influxd.bolt with https://github.com/br0xen/boltbrowser might help
