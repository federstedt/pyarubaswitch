# Get lldp neighbours, return port information for those neighbours
from .models import LldpNeighbour, LLDPTable

class LLdpInfo(object):

    def __init__(self, api_client):
        self.api_client = api_client

    def get_neighbours_sorted(self):
        '''Returns switch / ap object based on lldp discovery.
            Requires atleast rest-api version 4.
        '''
        # Kräver v4 för att funka snyggast, saknas en hel del annars

        lldp_json = self.api_client.get('lldp/remote-device')
        # if api_session was created within the object itself. Logout as it will not be reused outside this object
        if not self.api_client.error:
            elements = lldp_json['lldp_remote_device_element']
            lldp_table = LLDPTable()
            
            for x in elements:

                is_a_switch = x['capabilities_enabled']['bridge']
                is_a_phone = x['capabilities_enabled']['telephone']

                if is_a_switch == True and is_a_phone != True:
                    #TODO: kolla om v7 har name = chassi_id
                    # sometimes its a list, sometimes its a dict
                    if type(x['remote_management_address']) == list:
                        remote_ip = x['remote_management_address'][0]['address']
                    else:
                        remote_ip = x['remote_management_address']['address']

                    switch = LldpNeighbour(
                        local_port=x['local_port'], name=x['system_name'], ip_address=remote_ip,remote_port=x['port_id'])
                    lldp_table.switches.append(switch)

                is_an_ap = x['capabilities_enabled']['wlan_access_point']

                if is_an_ap == True:
                    if type(x['remote_management_address']) == list:
                        remote_ip = x['remote_management_address'][0]['address']
                    else:
                        remote_ip = x['remote_management_address']['address']
                    ap = LldpNeighbour(
                        local_port=x['local_port'], name=x['system_name'], ip_address=remote_ip)
                    lldp_table.access_points.append(ap)

            
            return lldp_table


        elif self.api_client.error:
            print(self.api_client.error)

    def get_neighbors(self):
        '''
        Get lldp info using legacy API. 
        Cannot sort APs from Switches by capability key
        '''
        lldp_json = self.api_client.get('lldp/remote-device')

        

        if not self.api_client.error:
            lldp_devs = []
            elements = lldp_json['lldp_remote_device_element']

            print(elements)
            for e in elements:

                lldp_neighbour = LldpNeighbour(local_port=e["local_port"],name=e["system_name"],remote_port=e["port_id"])
                lldp_devs.append(lldp_neighbour)
            
            return lldp_devs
        



