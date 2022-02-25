from pyarubaswitch_workflows.runner import Runner
from pyarubaswitch.aruba_switch_client import ArubaSwitchClient

from pprint import pprint

class TopologyMapper(Runner):

    def export_topology_csv(self, switchip, clients, wireless_clients, uplink_ports, wireless_ports):
        '''
        Exports topology data to csv-files
        '''
        #ip = switch
        # all clients on switch = clients
        # lldp-neighbours = lldp_data
        #TODO: exportera info med denna data



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

            print("Getting lldp data")
            if switch_client.api_client.legacy_api:
                lldp_data = self.get_lldp_info(switch_client)
            else:
                lldp_data = self.get_lldp_info_sorted(switch_client)

            pprint(lldp_data)
            uplink_ports = []
            wireless_ports = []

            # lldp-data can be a dict of: 
            # ap_list: [list-of,aps]
            # switch_list: [list-of,switches]
            # or if using legacy api, one big list of devices
            if switch_client.api_client.legacy_api:
                for entry in lldp_data:
                    uplink_ports.append(entry.local_port)
            else:
                for entry in lldp_data["ap_list"]:
                    wireless_ports.append(entry.local_port)
                for entry in lldp_data["switch_list"]:
                    uplink_ports.append(entry.local_port)
           
            
            clients = []
            for entry in mac_table:
                if entry.port_id not in uplink_ports and entry.port_id not in wireless_ports:
                    clients.append(entry)
            wireless_clients = []
            for entry in mac_table:
                if entry.port_id in wireless_ports:
                    wireless_clients.append(entry)
            
            # sorting wireless and wired clients only works if api has version4 or greater
            print("Wired clients")
            pprint(clients)
            print("WLAN clients")
            pprint(wireless_clients)

            
            self.export_topology_csv(switchip=switch, clients=clients, wireless_clients=wireless_clients, uplink_ports=uplink_ports, wireless_ports=wireless_ports)

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

    