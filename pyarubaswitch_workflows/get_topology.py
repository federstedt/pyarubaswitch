from pyarubaswitch_workflows.runner import Runner
from pyarubaswitch.aruba_switch_client import ArubaSwitchClient
import csv

from pprint import pprint



class SwitchInfo(object):


    def __repr__(self):
        return f"switch_ip: {self.switch_ip}\nclients: {self.clients}\nwireless_clients: {self.wireless_clients}\n lldp_devices: {self.lldp_devices}\nnumber_mac_antrys: {self.number_mac_entrys}"

    def __init__(self, switch_ip, clients, wireless_clients, lldp_devices, number_mac_entrys):
        self.switch_ip = switch_ip # switch ip address
        self.clients = clients # list of clients
        self.wireless_clients = wireless_clients # list of WLANclients
        self.lldp_devices = lldp_devices # list OR dict of lldp_devices. if dict = ap_list , switch_list LISTS
        self.number_mac_entrys = number_mac_entrys




class TopologyMapper(Runner):



    def __init__(self, config_filepath=None, site_name=None, export_folder_name="export", exlude_vlans=None, arg_username=None, arg_password=None,
                 arg_switches=None, SSL=False, verbose=False, timeout=5, validate_ssl=False, ssl_login=False, rest_version=7):
        super().__init__(config_filepath, arg_username, arg_password,
                 arg_switches, SSL, verbose, timeout, validate_ssl, ssl_login, rest_version)
        '''
        params: exlude_vlans , list or int . ignore clients on this vlan. ie [1,20] or 20 ignore clients on vlan 1 and 20 or 20.
        '''

        if self.args_passed == False:
            self.site_name = self.config.site_name
        else:
            self.site_name = site_name
        self.export_folder = export_folder_name
        self.exlude_vlans = []
        if type(exlude_vlans) == list:
            self.exlude_vlans = exlude_vlans
        elif type(exlude_vlans) == int:
            self.exlude_vlans.append(exlude_vlans)
        elif exlude_vlans == None:
            pass
        else:
            print(f'Incorrect type of param exlude_vlans: {type(exlude_vlans)}')


    def get_devices_csv(self, csv_filename):
        # read csv
        mac_list = []
        # add device mac-address to list

        # return list


    def export_topology_csv(self, topology_list):
        '''
        Exports topology data to csv-files
        filename is set by self.site_name, read from args to TopolgyMapper or from yaml file site_name
        '''
        # client file data export
        # mac-adress, port, wireless(YES/NO)
        client_header = ["switchip", "mac_address", "port","vlan_id", "Wireless"]
        client_file = f"{self.export_folder}/{self.site_name}_clients.csv"

        # check if there already is a file with Path
        #TODO: get device list with mac-adresses from csv


        with open(client_file, "w", encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(client_header)

            for switch_obj in topology_list:
                for client in switch_obj.clients:
                    row = [switch_obj.switch_ip, client.mac_address.replace("-",""), client.port_id, client.vlan_id, ""]
                    # check if device already excist in csv
                    # if excist update it. (device can change port) , do NOT append , update row

                    # if not excist before append
                    writer.writerow(row)

                for client in switch_obj.wireless_clients:
                    row = [switch_obj.switch_ip, client.mac_address.replace("-",""), client.port_id, client.vlan_id, "YES"]
                    writer.writerow(row)
            

        # uplink file data export
        uplink_header = ["switchip", "name", "port", "remote_port", "ip_address", "Type"]
        # append uplink_ports
        uplink_file = f"{self.export_folder}/{self.site_name}_netdevices.csv"
        # append ap_ports
        with open(uplink_file, "w", encoding="UTF8") as f:
            writer = csv.writer(f)
            writer.writerow(uplink_header)

            
            for switch_obj in topology_list:
                if "ap_list" in switch_obj.lldp_devices:
                    for ap in switch_obj.lldp_devices["ap_list"]:
                        row = [switch_obj.switch_ip, ap.name, ap.local_port, ap.remote_port, ap.ip_address, "AP"]
                        writer.writerow(row)
                if "switch_list" in switch_obj.lldp_devices:
                    for switch in switch_obj.lldp_devices["switch_list"]:
                        row = [switch_obj.switch_ip, switch.name, switch.local_port, switch.remote_port, switch.ip_address, "Switch"]
                        writer.writerow(row)
                
                if type(switch_obj.lldp_devices) == list:
                    for device in switch_obj.lldp_devices:
                        row = [switch_obj.switch_ip, device.name, device.local_port, device.remote_port, device.ip_address, ""]
                        writer.writerow(row)
    




    def get_topology(self):
        '''
        Maps network toplogy
        '''
        # create topology list to return
        topology = []
        # create apiclient objects
        for switch in self.switches:
            switch_client = ArubaSwitchClient(
                    switch, self.username, self.password, self.SSL, self.verbose, self.timeout, self.validate_ssl, self.rest_version)
            
            if self.verbose:
                print("Logging in...")
            switch_client.login()
            if switch_client.api_client.error:
                print("ERROR LOGIN:")
                print(switch_client.api_client.error)

            switch_client.set_rest_version()
            if switch_client.api_client.error:
                print("ERROR getting rest version:")
                print(switch_client.api_client.error)
            if self.verbose:
                print(f"Using rest-version: {switch_client.rest_version}")

            mac_table = self.get_mac_table(switch_client)

            print("Getting lldp data")
            if switch_client.api_client.legacy_api:
                lldp_data = self.get_lldp_info(switch_client)
            else:
                lldp_data = self.get_lldp_info_sorted(switch_client)

            
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
            ignored_entrys = []
            num_entrys = 0
            num_clients = 0
            for entry in mac_table:
                num_entrys += 1
                if entry.port_id not in uplink_ports and entry.port_id not in wireless_ports and entry.vlan_id not in self.exlude_vlans:
                    num_clients += 1
                    clients.append(entry)
                else:
                    ignored_entrys.append(entry)

            wireless_clients = []
            for entry in mac_table:
                if entry.port_id in wireless_ports and entry.vlan_id not in self.exlude_vlans:
                    wireless_clients.append(entry)
                else:
                    ignored_entrys.append(entry)

            
            # sorting wireless and wired clients only works if api has version4 or greater
            print("Wired clients")
            pprint(clients)
            print("WLAN clients")
            pprint(wireless_clients)
            print(f'Num ignored clients: {len(ignored_entrys)}')

            print(f"number of mac-entrys in table: {num_entrys}")
            print(f"number of wired clients on switch (as in exlude found on uplinkports): {num_clients}")
            # create switchobject
            sw_obj = SwitchInfo(switch_ip=switch, clients=clients, wireless_clients=wireless_clients, lldp_devices=lldp_data, number_mac_entrys=num_clients)
            topology.append(sw_obj)
            switch_client.logout()

        return topology





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

    


