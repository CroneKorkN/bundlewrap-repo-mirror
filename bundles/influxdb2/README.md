# setup

1. apply influxdb to server
2. write `admin`, `readonly` and `writeonly` token into influxdb metadata:
  `influx auth list --json | jq -r '.[] | select (.description == "NAME") | .token'`
3. apply clients

# metadata

```python
{
  'hostname': 'example.com',
  'admin_token': 'Wawbd5n...HJS76ez',
  'readonly_token': '5v235b3...6wbnuzz',
  'writeonly_token': '8w4cnos...fn849zg',
}
```

# reset password

Opening /var/lib/influxdb/influxd.bolt with https://github.com/br0xen/boltbrowser might help
