

from pyarubaswitch.config_reader import ConfigReader
from pyarubaswitch.input_parser import InputParser
# Sample runner for api


class Runner(object):

    def __init__(self, config_filepath=None, arg_username=None, arg_password=None,
                 arg_switches=None, SSL=False, verbose=False, timeout=10, validate_ssl=False, ssl_login=False, rest_version=7):

        if arg_username == None and arg_password == None and arg_switches == None:
            args_passed = False
        else:
            args_passed = True

        self.config_filepath = config_filepath
        if self.config_filepath != None:
            self.config = ConfigReader(self.config_filepath)
        elif args_passed == False:
            self.config = InputParser()
        else:
            self.username = arg_username
            self.password = arg_password
            self.switches = arg_switches

        if args_passed == False:
            self.username = self.config.username
            self.password = self.config.password
            self.switches = self.config.switches

        self.verbose = verbose
        self.timeout = timeout
        self.validate_ssl = validate_ssl
        self.ssl_login = ssl_login
        self.SSL = SSL
        self.rest_version = rest_version
