```python
{
    'apt': {
        'packages': {
            'apt-transport-https': {},
        },
        'sources': [
            # place key under data/apt/keys/packages.cloud.google.com.{asc|gpg}
            'deb https://packages.cloud.google.com/apt cloud-sdk main',
        ],
    },
}
```
