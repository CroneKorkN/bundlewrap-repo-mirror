from mako.template import Template
from copy import deepcopy


def generate_flux(bucket, host, field, data):
    return Template(flux_template).render(
        bucket=bucket,
        host=host,
        field=field,
        data=data
    ).strip()


def generate_panel(bucket, host, title, targets, min=None, max=None):
    panel = deepcopy(panel_template)
    panel['title'] = title
    
    if min:
        panel['fieldConfig']['defaults']['min'] = min
    if max:
        panel['fieldConfig']['defaults']['max'] = max

    panel['targets'] = [
        {
            'hide': False,
            'refId': field,
            'query': generate_flux(bucket, host, field, data),
        } for field, data in targets.items()
    ]
