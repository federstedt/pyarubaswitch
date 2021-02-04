from pathlib import Path
import yaml


class ConfigReader(object):

    def __init__(self, filepath):

        self.filepath = filepath

        # try to read file, if doesnt exist. exit app
        if Path(self.filepath).is_file():
            self.vars = self.read_yaml(self.filepath)

            self.username = self.vars["username"]
            self.password = self.vars["password"]
            self.switches = self.vars["switches"]
        else:
            print("Error! No configfile was found:")
            print(self.filepath)
            exit(0)

    def read_yaml(self, filename):
        '''Get username password and IP of switches from file '''
        with open(filename, "r") as input_file:
            data = yaml.load(input_file, Loader=yaml.FullLoader)
        return data
