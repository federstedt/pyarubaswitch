# Get lldp neighbours, return port information for those neighbours
from .models import LldpNeighbour

class LLdpInfo(object):

    def __init__(self, api_client):
        self.api_client = api_client

    def get_neighbours_sorted(self, capability="all"):
        '''Returns switch / ap object based on lldp discovery.
            Requires atleast rest-api version 4.
            :params capability , defualt="all" get switches and aps. Set to "ap" for aps, or "switch" for switches.
        '''
        # Kräver v4 för att funka snyggast, saknas en hel del annars

        # converts to lower just in case user specifies uppercase
        capability = capability.lower()
        lldp_json = self.api_client.get('lldp/remote-device')
        # if api_session was created within the object itself. Logout as it will not be reused outside this object
        if not self.api_client.error:
            elements = lldp_json['lldp_remote_device_element']
            switches = []
            access_points = []

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
                    switches.append(switch)

                is_an_ap = x['capabilities_enabled']['wlan_access_point']

                if is_an_ap == True:
                    if type(x['remote_management_address']) == list:
                        remote_ip = x['remote_management_address'][0]['address']
                    else:
                        remote_ip = x['remote_management_address']['address']
                    ap = LldpNeighbour(
                        local_port=x['local_port'], name=x['system_name'], ip_address=remote_ip)
                    access_points.append(ap)

            if capability == "all":
                return({'ap_list': access_points, 'switch_list': switches})
            elif capability == "ap":
                return access_points
            elif capability == "switch":
                return switches
        elif self.api_client.error:
            print(self.api_client.error)

    def get_neighbors(self, capability="all"):
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
        



