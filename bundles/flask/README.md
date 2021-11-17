# Flask

This bundle can deploy one or more Flask applications per node.

```python
    'flask': {
        'myapp': {
            'app_module': "myapp",
            'apt_dependencies': [
                "libffi-dev",
                "libssl-dev",
            ],
            'env': {
                'APP_SECRETS': "/opt/client_secrets.json",
            },
            'json_config': {
                'this json': 'is_visible',
                'inside': 'your template.cfg',
            },
            'git_url': "ssh://git@bitbucket.apps.seibert-media.net:7999/smedia/myapp.git",
            'git_branch': "master",
            'deployment_triggers': ["action:do-a-thing"],
        },
    },
```

The git repo containing the application has to obey some conventions:

* requirements-frozen.txt (preferred) or requirements.txt
* minimal setup.py to allow for installation with pip

The `app` instance has to exists in the module defined by `app_module`.

It is also very advisable to enable logging in your app (otherwise HTTP 500s won't be logged):

```python
import logging

if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)
```

If you specify `json_config`, then `/opt/${app}/config.json` will be
created. The environment variable `$APP_CONFIG` will point to the exact
name. You can use it in your app to load your config:

```python
app.config.from_json(environ['APP_CONFIG'])
```

If `json_config` is *not* specified, you *can* put a static file in
`data/flask/files/cfg/$app_name`.
