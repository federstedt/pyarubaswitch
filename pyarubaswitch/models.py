from pydantic import BaseModel

class SystemInfo(BaseModel):
    name: str
    hw_rev: str
    fw_ver: str
    serial: str
    mac_addr: str

class MacTableElement(BaseModel):
    mac_address: str
    port_id: str
    vland_id: int


class STP(BaseModel):
    enabled: bool
    prio: int
    mode: str

class LldpNeighbour(BaseModel):
    local_port: str
    name: str
    ip_address: str
    remote_port: str | None

class LLDPTable(BaseModel):
    switches: list[LldpNeighbour] = []
    access_points: list[LldpNeighbour] = []


class Transceiver(BaseModel):
    part_number: str
    port_id: int
    product_number: str
    serial_number: str
    trans_type: str

class SntpServer(BaseModel):
    address: str | None
    prio: int | None


class Snmpv3(BaseModel):
    enabled: bool
    readonly: bool
    only_v3: bool