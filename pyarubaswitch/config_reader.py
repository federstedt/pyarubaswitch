from pathlib import Path
import yaml

from pyarubaswitch.aruba_switch_client import ArubaSwitchClient

class ConfigReader(object):

    def __init__(self, filepath):

        self.filepath = filepath

        # try to read file, if doesnt exist. exit app
        if Path(self.filepath).is_file():
            self.vars = self.read_yaml(self.filepath)

            self.username = self.vars["username"]
            self.password = self.vars["password"]
            self.switches = self.vars["switches"]
            if "site_name" in self.vars:
                self.site_name = self.vars["site_name"]
        else:
            print("Error! No configfile was found:")
            print(self.filepath)
            exit(0)

    def read_yaml(self, filename):
        '''Get username password and IP of switches from file '''
        with open(filename, "r") as input_file:
            data = yaml.load(input_file, Loader=yaml.FullLoader)
        return data

    def get_apiclient_from_file(self, ip_addr: str, verbose: bool = False, SSL: bool = False, timeout: int = 15):
        '''
        Takes yaml file, returns ArubaSwitchClient object
        args:
        ip_addr : str format ip-adress of switch to return a client
        '''
        return ArubaSwitchClient(switch_ip=ip_addr, username=self.username, password=self.password,verbose=verbose, SSL=SSL, timeout=timeout)




