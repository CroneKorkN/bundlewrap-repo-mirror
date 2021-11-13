from configparser import ConfigParser
import json

def parse(text):
    config = ConfigParser()
    config.read_string(text)
    
    return {
        section: dict(config.items(section))
            for section in config.sections()
    }

class Writable():
    data = ''

    def write(self, line):
        self.data += line

def dumps(dict):
    config = ConfigParser()
    sorted_dict = json.loads(json.dumps(dict, sort_keys=True))
    config.read_dict(sorted_dict)
    writable = Writable()
    config.write(writable)

    return writable.data
