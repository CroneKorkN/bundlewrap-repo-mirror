"""local: identifier of the bw host itself (read from ~/.config/bundlewrap/local_id) — paired with hooks/skip_local_nodes.py."""

from os.path import expanduser, exists
from functools import cache

@cache
def id():
    if exists(expanduser('~/.config/bundlewrap/local_id')):
        with open(expanduser('~/.config/bundlewrap/local_id'), 'r') as file:
            return file.read().strip()
