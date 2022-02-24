from pyarubaswitch_workflows.runner import Runner
from pyarubaswitch.aruba_switch_client import ArubaSwitchClient

from pprint import pprint

class TopologyMapper(Runner):

    def export_topology_csv(self, mac_table):
        '''
        Exports topology data to csv-files
        '''



    def get_topology(self):
        '''
        Maps network toplogy
        '''
        # create apiclient objects
        for switch in self.switches:
            switch_client = ArubaSwitchClient(
                    switch, self.username, self.password, self.SSL, self.verbose, self.timeout, self.validate_ssl, self.rest_version)
            
            if self.verbose:
                print("Logging in...")
            switch_client.login()

            switch_client.set_rest_version()
            if self.verbose:
                print(f"Using rest-version: {switch_client.rest_version}")

            mac_table = self.get_mac_table(switch_client)

            #self.export_topology_csv(mac_table)
       
            lldp_data = self.get_lldp_info(switch_client)
            pprint(lldp_data)
            switch_ports = []
            for dev in lldp_data:
                switch_ports.append(dev.local_port)
            
            clients = []
            for entry in mac_table:
                if entry.port_id not in switch_ports:
                    clients.append(entry)

            #ip = switch
            # all clients on switch = clients
            # lldp-neighbours = lldp_data
            #TODO: exportera info med denna data

            switch_client.logout()





    def get_mac_table(self, api_runner):
        '''
        :params api_runner   ArubaSwitchClient object
        Get mac-address table from switch
        '''
        switch_client = api_runner
               
        if switch_client.api_client.error:
            print(switch_client.api_client.error)
            exit(0)

        if self.verbose:
            print("Getting mac-address table")
        mac_table = switch_client.get_mac_address_table()

        return mac_table

    