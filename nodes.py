from os import walk
from os.path import join, basename, splitext


for root, dirs, files in walk(join(repo_path, "nodes")):
    for filename in files:
        if filename.endswith(".py"):
            node = join(root, filename)
            with open(node, 'r', encoding='utf-8') as f:
                nodes[splitext(basename(filename))[0]] = eval(f.read())
