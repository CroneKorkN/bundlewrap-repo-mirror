# SYSTEMD

## show unit paths

```
systemctl --no-pager --property=UnitPath show | tr ' ' '\n'
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
