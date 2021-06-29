from os import walk
from os.path import join, basename, splitext

converters = {
    '32_random_bytes_as_base64_for': lambda x: vault.random_bytes_as_base64_for(x, length=32),
    'decrypt': lambda x: vault.decrypt(x),
    'decrypt_file': lambda x: vault.decrypt_file(x),
    'password_for': lambda x: vault.password_for(x),
}

def demagify(data):
    if isinstance(data, str):
        for name, converter in converters.items():
            if data.startswith(f'!{name}:'):
                return converter(data[len(name) + 2:])
        else:
            return data
    elif isinstance(data, dict):
        return type(data)({key: demagify(value) for key, value in data.items()})
    elif isinstance(data, (list, set, tuple)):
        return type(data)([demagify(element) for element in data])
    else:
        return data

for root, dirs, files in walk(join(repo_path, "nodes")):
    for filename in files:
        if filename.endswith(".py"):
            node = join(root, filename)
            with open(node, 'r', encoding='utf-8') as f:
                nodes[splitext(basename(filename))[0]] = demagify(eval(f.read()))
