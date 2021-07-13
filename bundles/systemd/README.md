# SYSTEMD

## metadata

```python
{
    'systemd': {
        'units': {
            'test.service': {
                # optional: will be derived from unit extension
                'path': '/etc/systemd/system/test.service',
                # content of the unit file
                'content': {
                },
                # bw item data
                # applies to unitfile and svc_systemd aswell, if present
                'item': {
                },
            }
        }
    },
}
```
