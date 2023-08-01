# https://manpages.debian.org/latest/apt/sources.list.5.de.html
# https://repolib.readthedocs.io/en/latest/deb822-format.html

```python
{
    'apt': {
        'packages': {
            'apt-transport-https': {},
        },
        'sources': {
            'debian': {
                'types': { # optional, defaults to `{'deb'}``
                    'deb',
                    'deb-src',
                },
                'urls': {
                    'https://deb.debian.org/debian',
                },
                'suites': { # at least one
                    '{codename}',
                    '{codename}-updates',
                    '{codename}-backports',
                },
                'components': { # optional
                    'main',
                    'contrib',
                    'non-frese',
                },
                # key:
                # - optional, defaults to source name (`debian` in this example)
                # - place key under data/apt/keys/debian-12.{asc|gpg}
                'key': 'debian-{version}',
            },
        },
    },
}
```
