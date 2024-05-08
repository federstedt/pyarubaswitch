from typing import List

from pydantic import BaseModel

from .pyaos_switch_client import PyAosSwitchClient


class MacTable(BaseModel):
    mac_address: str
    port_id: str
    vlan_id: int

class MacAddressTable(BaseModel):
    mac_table: List[MacTable]
    @classmethod
    def from_api(cls, api_client:PyAosSwitchClient) -> List[MacTable]:
        mac_elements = cls.get_mac_table(api_client)
        mac_table = [MacTable(**entry) for entry in mac_elements]
        return cls(mac_table=mac_table)
    
    @classmethod
    def get_mac_table(cls,api_client:PyAosSwitchClient) -> 'MacAddressTable':
        return api_client.get('mac-table')['mac_table_entry_element']
    
class InterfaceMacTable(BaseModel):
    mac_table: List[MacTable]
    @classmethod
    def from_api(cls, api_client:PyAosSwitchClient) -> List[MacTable]:
        mac_elements = cls.get_interface_mac_table(api_client)
        mac_table = [MacTable(**entry) for entry in mac_elements]
        return cls(mac_table=mac_table)
    
    @classmethod
    def get_interface_mac_table(cls,api_client:PyAosSwitchClient) -> 'InterfaceMacTable':
        return api_client.get('mac-table')['mac_table_entry_element']
