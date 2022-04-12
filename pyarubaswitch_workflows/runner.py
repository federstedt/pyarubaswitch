
from pyarubaswitch import ArubaSwitchClient
from pyarubaswitch.config_reader import ConfigReader
from pyarubaswitch.input_parser import InputParser
# Sample runner for api

from pyarubaswitch_workflows.network_objects import SwitchInfo

class Runner(object):

    def __init__(self, config_filepath=None, arg_username=None, arg_password=None,
                 arg_switches=None, SSL=False, verbose=False, timeout=5, validate_ssl=False, ssl_login=False, rest_version=7):

        if arg_username == None and arg_password == None and arg_switches == None:
            self.args_passed = False
        else:
            self.args_passed = True

        self.config_filepath = config_filepath
        if self.config_filepath != None:
            self.config = ConfigReader(self.config_filepath)
        elif self.args_passed == False:
            self.config = InputParser()
        else:
            self.username = arg_username
            self.password = arg_password
            self.switches = arg_switches

        if self.args_passed == False:
            self.username = self.config.username
            self.password = self.config.password
            self.switches = self.config.switches

        self.verbose = verbose
        self.timeout = timeout
        self.validate_ssl = validate_ssl
        self.ssl_login = ssl_login
        self.SSL = SSL
        self.rest_version = rest_version


        
    def get_lldp_info_sorted(self, api_runner):
        '''
        Legacy API cannot detect capability ie switch or ap (pre v4)
        :param api_runner , aruba_switch_client api client object.
        :return lldp info
        '''
        if api_runner.api_client.legacy_api:
            print("API running legacy apiversion pre v4.\nWill return unsorted list of devices")
            lldp_data = self.get_lldp_info(api_runner)
        else:
            lldp_data = api_runner.get_lldp_info_sorted()
            
        
        return lldp_data

    def get_lldp_info(self, api_runner):
        '''
        :param api_runner , aruba_switch_client api client object.
        :return lldp info
        '''
        lldp_dev = api_runner.get_lldp_info()
        return lldp_dev



    def get_vlans_lldp_neighbours(self, api_runner, lldp_aps, lldp_switches):
        for ap in lldp_aps:
            ap_port_data = api_runner.get_port_vlan(ap.local_port)
            print(f"{ap.name}")
            print(ap_port_data)
        for sw in lldp_switches:
            switch_port_data = api_runner.get_port_vlan(sw.local_port)
            print(sw.name)
            print(switch_port_data)


    def get_transceivers(self):
        ''' 
        Get transievers from all switches.
        return list of switch objects, populated with switch.transceivers
        '''
        
        switches = []
        for switch in self.switches:
            switch_client = ArubaSwitchClient(
                    switch, self.username, self.password, self.SSL, self.verbose, self.timeout, self.validate_ssl, self.rest_version)
            switch_client.login()

            print(f"Getting transceivers from switch: {switch}")
            transceivers_data = switch_client.get_transceivers()
            switch_obj = SwitchInfo(switch_ip=switch, transceivers=transceivers_data)
            switches.append(switch_obj)

            switch_client.logout()

        return switches
            
