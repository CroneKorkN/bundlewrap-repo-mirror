from mako.template import Template

template = '''
% for segment, options in sorted(data.items()):

%     if '#' in segment:
# ${segment.split('#', 2)[1]}
%     endif
[${segment.split('#')[0]}]
%     for option, value in options.items():
%         if isinstance(value, dict):
%             for k, v in value.items():
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

def generate_unitfile(data):
    return Template(template).render(data=data).lstrip()
