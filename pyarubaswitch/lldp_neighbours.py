# Get lldp neighbours, return port information for those neighbours
from pyarubaswitch.api_engine import APIuser


class LLdpInfo(APIuser):

    def get_neighbors(self, capability="all"):
        '''Returns switch / ap object based on lldp discovery.'''
        # Kräver v4 för att funka snyggast, saknas en hel del annars

        # converts to lower just in case user specifies uppercase
        capability = capability.lower()
        lldp_json = self.api_client.get('lldp/remote-device')
        # if api_session was created within the object itself. Logout as it will not be reused outside this object
        if self.api_passed == False:
            self.api_client.logout()

        elements = lldp_json['lldp_remote_device_element']

        switches = []
        access_points = []

        for x in elements:

            is_a_switch = x['capabilities_enabled']['bridge']

            if is_a_switch == True:
                #DEBUG: print('Switch: ' + 'localport: ' + x['local_port'] + ' remoteport: ' + x['port_id'] + ' neighbor name: ' + x['chassis_id'] + ' neighbor ip: ' + x['remote_management_address']['address'] + '\n')
                switch = LldpSwitch(
                    x['local_port'], x['port_id'], x['chassis_id'], x['remote_management_address'][0]['address'])
                # switches.append({'local_port': x['local_port'],
                #                 'remote_port': x['port_id'],
                #                 'name': x['chassis_id'],
                #                 'ip': x['remote_management_address']['address']})
                switches.append(switch)

            is_an_ap = x['capabilities_enabled']['wlan_access_point']

            if is_an_ap == True:
                #DEBUG: print('AccessPoint: ' + 'localport: ' + x['local_port'] + ' AP-name: ' + x['system_name'])
                ap = LldpAccessPoints(
                    x['local_port'], x['system_name'], x['remote_management_address'][0]['address'])
                # access_points.append({'local_port': x['local_port'],
                #                      'name': x['system_name'],
                #                      'ip': x['remote_management_address']['address']})
                access_points.append(ap)

        if capability == "all":
            return({'ap_list': access_points, 'switch_list': switches})
        elif capability == "ap":
            return access_points
        elif capability == "switch":
            return switches


class LldpNeighbour(object):

    def __init__(self, local_port, name, ip):
        self.local_port = local_port
        self.name = name
        self.ip = ip

    def __repr__(self):
        return f"name: {self.name}, local_port: {self.local_port}, ip_address: {self.ip}"


class LldpAccessPoints(LldpNeighbour):
    pass


class LldpSwitch(LldpNeighbour):

    def __init__(self, local_port, remote_port, name, ip):
        self.remote_port = remote_port
        super(LldpSwitch, self).__init__(local_port, name, ip)

    def __repr__(self):
        return f"name: {self.name}, local_port: {self.local_port},remote_port: {self.remote_port}, ip_address: {self.ip}"
