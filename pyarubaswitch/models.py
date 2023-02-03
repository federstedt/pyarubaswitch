from pydantic import BaseModel

class SystemInfo(BaseModel):
    name: str
    hw_rev: str
    fw_ver: str
    serial: str
    mac_addr: str


class MacTableElement(object):

    def __repr__(self):
        return f"mac_address: {self.mac_address}, port_id: {self.port_id}, vlan_id: {self.vlan_id}"

    def __init__(self, mac_address, port_id, vlan_id, switch_ip=None):
        self.mac_address = mac_address
        self.port_id = port_id
        self.vlan_id = vlan_id
        self.switch_ip = switch_ip # optional switch where client was found


class Snmpv3(object):

    def __repr__(self):
        return f"enabled: {self.enabled}, is_non_v3_readonly: {self.non_snmpv3_readonly}, only_v3: {self.only_v3}"

    def __init__(self, enabled, readonly, only_v3):
        self.enabled = enabled
        self.non_snmpv3_readonly = readonly
        self.only_v3 = only_v3


class SntpServer(object):

    def __repr__(self):
        return f"address: {self.address}, prio: {self.prio}"

    def __init__(self, address, prio):
        self.address = address
        self.prio = prio

class STP(BaseModel):
    enabled: bool
    prio: int
    mode: str


class Transceiver(object):

    def __repr__(self):
        return f"Transceiver: part_number: {self.part_number}, port_id: {self.port_id}, product_number: {self.product_number}, serial_number: {self.serial_number}, type: {self.type}" 

    def __init__(self, part_number, port_id, product_number, serial_number, trans_type):
        self.part_number = part_number
        self.port_id = port_id
        self.product_number = product_number
        self.serial_number = serial_number
        self.type = trans_type


class LldpNeighbour(object):

    def __init__(self, local_port, name, ip_address=None, remote_port=None):
        self.local_port = local_port
        self.name = name
        self.ip_address = ip_address
        self.remote_port = remote_port

    def __repr__(self):
        return f"name: {self.name}, local_port: {self.local_port}, remote_port: {self.remote_port}, ip_address: {self.ip_address}"