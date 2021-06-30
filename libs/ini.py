from configparser import ConfigParser

class Writable():
    data = ''
    
    def write(self, line):
        self.data += line

def dumps(dict):
    config = ConfigParser()
    
    for section, settings in dict.items():
        config[section] = settings

    writable = Writable()
    config.write(writable)

    return writable.data
