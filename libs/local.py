from os.path import expanduser, exists
from functools import cache

@cache
def id():
    if exists(expanduser('~/.config/bundlewrap/local_id')):
        with open(expanduser('~/.config/bundlewrap/local_id'), 'r') as file:
            return file.read().strip()
