# a class that has a lot of methods for getting relevant data from the api client
# uses the client to pass a api_client object, object is used for running calls for getting the data
from pyarubaswitch.api_engine import PyAosSwitch

from pyarubaswitch.system_status import SystemStatus
from pyarubaswitch.lldp_neighbours import LLdpInfo
from pyarubaswitch.get_port_vlans import Vlaninfo
from pyarubaswitch.telnet_info import TelnetInfo
from pyarubaswitch.get_stp_info import StpInfo
from pyarubaswitch.get_snmpv3_info import Snmpv3Info
from pyarubaswitch.get_sntp import SntpInfo
from pyarubaswitch.get_loop_protect import LoopProtect


class ArubaSwitchClient(object):

    def __init__(self, switch_ip, username, password, SSL=False, verbose=False, timeout=10, validate_ssl=False, rest_version=7):
        self.switch_ip = switch_ip
        self.username = username
        self.password = password
        self.SSL = SSL
        self.timeout = timeout
        self.verbose = verbose
        self.validate_ssl = validate_ssl
        self.rest_version = rest_version
        self.api_client = PyAosSwitch(
            switch_ip, self.username, self.password, SSL=self.SSL, verbose=self.verbose, timeout=self.timeout,
            validate_ssl=self.validate_ssl, rest_version=self.rest_version)

    def get_system_status(self):
        '''Returns SystemInfo object with name, firmware status etc'''
        system_info = SystemStatus(apiclient=self.api_client)
        return system_info.get_system_info()

    def get_telnet_server_status(self):
        '''Returns true / false status of telnet server'''
        telnet_status = TelnetInfo(apiclient=self.api_client)
        return telnet_status.get_telnet_status()

    def get_stp_info(self):
        '''Returns stp-object containing stp-info.'''
        stp = StpInfo(apiclient=self.api_client)
        return stp.get_stp_info()

    def get_lldp_info(self):
        '''Returns all switch/ap neighbour info as objects '''
        lldp = LLdpInfo(apiclient=self.api_client)
        return lldp.get_neighbors(capability="all")

    def get_lldp_aps(self):
        '''Returns lldp neighbour objects. That are classified as APs'''
        lldp = LLdpInfo(apiclient=self.api_client)
        return lldp.get_neighbors(capability="ap")

    def get_lldp_switches(self):
        '''Returns lldp neighbour objects. That are classified as Switches'''
        lldp = LLdpInfo(apiclient=self.api_client)
        return lldp.get_neighbors(capability="switch")

    def get_port_vlan(self, port):
        '''Returns port info object, containing all vlans on that port untag/tagged'''
        vlan_info = Vlaninfo(apiclient=self.api_client)
        port_info = vlan_info.port_vlans(port)
        return port_info

    def get_snmpv3(self):
        '''Returns snmpv3 info object'''
        snmpv3_info = Snmpv3Info(apiclient=self.api_client)
        return snmpv3_info.get_snmpv3_info()

    def get_sntp(self):
        '''Returns sntp server, list of objects with sntp-server info.'''
        sntp_servers = SntpInfo(apiclient=self.api_client)
        return sntp_servers.get_sntp_info()

    def get_loop_protected_ports(self):
        ''' Returns list of loop-protected ports'''
        loop_protect = LoopProtect(apiclient=self.api_client)
        return loop_protect.get_protected_ports()

    def logout(self):
        '''Logout from switch '''
        self.api_client.logout()

    def login(self):
        '''Manually logon to the switch. Optional as API-client will login automatically.'''
        self.api_client.login()
