from configparser import ConfigParser

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
    config.read_dict(dict)
    writable = Writable()
    config.write(writable)

    return writable.data
