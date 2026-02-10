https://github.com/SirPlease/L4D2-Competitive-Rework/blob/master/Dedicated%20Server%20Install%20Guide/README.md

```python
    'tick60_maps': {
        'port': 27030,
        # add command line arguments
        'arguments': ['-tickrate 60'],
        # stack overlays, first is uppermost
        'overlays': ['tickrate', 'standard'],
        # server.cfg contents
        'config': [
            # configs from overlays are accessible via server_${overlay}.cfg
            'exec server_tickrate.cfg',
            # add more options
            'sv_minupdaterate 101',
            'sv_maxupdaterate 101',
            'sv_mincmdrate 101',
            'sv_maxcmdrate 101',
            'sv_consistency 0',
        ],
    },
```