

from pyarubaswitch.config_reader import ConfigReader
from pyarubaswitch.input_parser import InputParser
# Sample runner for api


class Runner(object):

    def __init__(self, config_filepath=None, arg_username=None, arg_password=None, arg_switches=None, verbose=False):

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
