from pyarubaswitch_workflows.runner import Runner
from pyarubaswitch.aruba_switch_client import ArubaSwitchClient


class TopologyMapper(Runner):

    def get_mac_table(self):
        '''
        Get mac-address table from switch
        '''
        for switch in self.switches:
            switch_client = ArubaSwitchClient(
                    switch, self.username, self.password, self.SSL, self.verbose, self.timeout, self.validate_ssl, self.rest_version)
            
            if self.verbose:
                print("Logging in...")
            switch_client.login()

            if self.verbose:
                print("Getting mac-address table")
            mac_table = switch_client.get_mac_address_table()
            return mac_table

