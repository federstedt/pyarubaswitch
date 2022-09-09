class SwitchInfo(object):


    def __repr__(self):
        return f"switch_ip: {self.switch_ip}\nclients: {self.clients}\nwireless_clients: {self.wireless_clients}\n lldp_devices: {self.lldp_devices}\nnumber_mac_antrys: {self.number_mac_entrys}\ntransceivers: {self.transceivers}"

    def __init__(self, switch_ip, clients=None, wireless_clients=None, lldp_devices=None, number_mac_entrys=None, transceivers=None, unmanaged_neighbor_ports=None):
        self.switch_ip = switch_ip # switch ip address
        self.clients = clients # list of clients
        self.wireless_clients = wireless_clients # list of WLANclients
        self.lldp_devices = lldp_devices # list OR dict of lldp_devices. if dict = ap_list , switch_list LISTS
        self.number_mac_entrys = number_mac_entrys
        self.transceivers = transceivers # list of transceivers on switch
        self.unmanaged_neighbor_ports = unmanaged_neighbor_ports # list of ports that has suspected unmanaged networkdevice connected