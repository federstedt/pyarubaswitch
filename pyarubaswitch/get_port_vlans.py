# get vlans for specified port
from pyarubaswitch.api_engine import APIuser


class Vlaninfo(APIuser):

    @property
    def vlan_data(self):
        ''' returns port objects with vlan info.'''
        vlan_info = self.api_client.get('vlans-ports')
        # if api_session was created within the object itself. Logout as it will not be reused outside this object
        if self.api_passed == False:
            self.api_client.logout()
        return vlan_info

    def port_vlans(self, interface):
        ''' Returns vlans configured on specified interface '''

        vlanelements = self.vlan_data['vlan_port_element']
        untag = []
        tag = []
        for x in vlanelements:
            port = x['port_id']
            vlanid = x['vlan_id']
            portmode = x['port_mode']

            if port == interface:
                # print('Portid:',port,'vlanid:',vlanid,'portmode:',portmode)   # Troubleshooting? print this...
                if portmode == 'POM_UNTAGGED':
                    untag.append(vlanid)
                if portmode == 'POM_TAGGED_STATIC':
                    tag.append(vlanid)

        port_object = Port(interface, untag, tag)
        return port_object


class Port(object):

    def __repr__(self):
        return f"Port: {self.id}, untagged: {self.untagged}, tagged: {self.tagged}"

    def __init__(self, port_id, untagged, tagged):
        self.id = port_id
        self.untagged = untagged
        self.tagged = tagged
        self.missing_untagged = []
        self.missing_tagged = []

    def check_desired_vlans(self, desired_untag, desired_tag):
        '''Returns missing vlans that are defined as desired untag/tag '''
        for vlan in desired_untag:
            if vlan not in self.untagged:
                self.missing_untagged.append(vlan)
        for vlan in desired_tag:
            if vlan not in self.tagged:
                self.missing_tagged.append(vlan)

        return self.missing_untagged, self.missing_tagged
