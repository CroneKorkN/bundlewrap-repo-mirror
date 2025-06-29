from configparser import ConfigParser
import json
from bundlewrap.metadata import MetadataJSONEncoder


class Writable():
    data = ''
    def write(self, line):
        self.data += line

class CaseSensitiveConfigParser(ConfigParser):
    # dont make keys lowercase
    def optionxform(self, value):
        return value

def parse(text):
    config = CaseSensitiveConfigParser(allow_no_value=True)
    config.read_string(text)

    return {
        section: dict(config.items(section))
            for section in config.sections()
    }

def dumps(dict):
    sorted_dict = json.loads(json.dumps(dict, sort_keys=True, cls=MetadataJSONEncoder))
    parser = CaseSensitiveConfigParser(allow_no_value=True)
    parser.read_dict(sorted_dict)

    writable = Writable()
    parser.write(writable)

    return writable.data
