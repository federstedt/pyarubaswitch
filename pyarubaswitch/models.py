from pydantic import BaseModel

class SystemInfo(BaseModel):
    name: str
    hw_rev: str
    fw_ver: str
    serial: str
    mac_addr: str

class MacTableElement(BaseModel):
    mac_address: str
    port_id: int
    vland_id: int


class STP(BaseModel):
    enabled: bool
    prio: int
    mode: str



class LldpNeighbour(BaseModel):
    local_port: int
    name: str
    ip_address: str
    remote_port: int | None

class LLDPTable(BaseModel):
    switches: list[LldpNeighbour] = []
    access_points: list[LldpNeighbour] = []

#TODO: nedan gör om till BaseModels

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


class Transceiver(object):

    def __repr__(self):
        return f"Transceiver: part_number: {self.part_number}, port_id: {self.port_id}, product_number: {self.product_number}, serial_number: {self.serial_number}, type: {self.type}" 

    def __init__(self, part_number, port_id, product_number, serial_number, trans_type):
        self.part_number = part_number
        self.port_id = port_id
        self.product_number = product_number
        self.serial_number = serial_number
        self.type = trans_type


