{
#    'id': 1,
#    'title': 'TBD',
    "gridPos": {
#        "x": 0,
#        "y": 0,
        "h": 8,
#        "w": 24
    },
    'type': 'timeseries',
    'transformations': [],
    'description': '',
    'fieldConfig': {
        'defaults': {
            'custom': {
                'drawStyle': 'line',
                'lineInterpolation': 'smooth',
                'barAlignment': 0,
                'lineWidth': 1,
                'fillOpacity': 40,
                'gradientMode': 'opacity',
                'spanNulls': False,
                'showPoints': 'never',
                'pointSize': 5,
                'stacking': {
                    'mode': 'none',
                    'group': 'A'
                },
                'axisLabel': '',
                'scaleDistribution': {
                    'type': 'linear'
                },
                'hideFrom': {
                    'tooltip': False,
                    'viz': False,
                    'legend': False
                },
                'thresholdsStyle': {
                    'mode': 'off',
                },
                'lineStyle': {
                    'fill': 'solid',
                },
            },
            'color': {
                'mode': 'palette-classic',
            },
            'mappings': [],
            'displayName': '${__field.name}',
        },
        'overrides': [],
    },
    'options': {
        'tooltip': {
            'mode': 'single',
        },
        'legend': {
            'displayMode': 'list',
            'placement': 'bottom',
            'calcs': [],
        },
    },
    'targets': [],
    'transparent': True,
    'datasource': None,
}
