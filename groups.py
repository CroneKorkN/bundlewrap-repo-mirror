from os import walk
from os.path import join, basename, splitext

for root, dirs, files in walk(join(repo_path, "groups")):
    for filename in files:
        if filename.endswith(".py"):
            group = join(root, filename)
            with open(group, 'r', encoding='utf-8') as f:
                try:
                    groups[splitext(basename(filename))[0]] = eval(f.read())
                except:
                    print(f"Error parsing {group}:")
                    raise
