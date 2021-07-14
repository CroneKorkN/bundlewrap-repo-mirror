from mako.template import Template

template = '''
% for segment, options in data.items():

%     if '#' in segment:
# ${segment.split('#', 2)[1]}
%     endif
[${segment.split('#')[0]}]
%     for option, value in sorted(options.items()):
%         if isinstance(value, dict):
%             for k, v in sorted(value.items()):
${option}=${k}=${v}
%             endfor
%         elif isinstance(value, (list, set, tuple)):
%             for item in sorted(value):
${option}=${item}
%             endfor
%         else:
${option}=${str(value)}
%         endif
%     endfor
% endfor
'''

order = [
    'Unit',
    'Timer',
    'Service',
    'Install',
]

def segment_order(segment):
    return (
        order.index(segment[0]) if segment[0] in order else float('inf'),
        segment[0]
    )

def generate_unitfile(data):
    return Template(template).render(
        data=dict(sorted(data.items(), key=segment_order)),
        order=order
    ).lstrip()
