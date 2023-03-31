# SYSTEMD

## show unit paths

```
systemctl --no-pager --property=UnitPath show --value | tr ' ' '\n'
```

## metadata

```python
{
    'systemd': {
        'units': {
            'test.service': {
            }
        }
    },
}
```
