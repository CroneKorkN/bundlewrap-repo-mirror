import yaml, json
from bundlewrap.metadata import MetadataJSONEncoder

files = {
    '/etc/icingadb/config.yml': {
        'content': yaml.dump(
            json.loads(
                json.dumps(node.metadata.get('icingadb'), sort_keys=True, cls=MetadataJSONEncoder)
            ),
        ),
        'mode': '0640',
        'owner': 'icingadb',
    },
}
