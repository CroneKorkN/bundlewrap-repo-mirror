from mako.template import Template

template = '''
% for i, (segment, options) in enumerate(data.items()):

[${segment}]
%     for option, value in options.items():
%         if isinstance(value, dict):
%             for k, v in value.items():
${option}=${k}=${v}
%             endfor
%         elif isinstance(value, (list, set, tuple)):
%             for item in sorted(value):
${option}=${item}
%             endfor
%         elif isinstance(value, str):
${option}=${value}
%         endif
%     endfor
% endfor
'''

def generate_unitfile(data):
    return Template(template).render(data=data).lstrip()
