from typing import List, Optional

from pydantic import BaseModel

from .pyaos_switch_client import PyAosSwitchClient

class Transceiver(BaseModel):
    part_number: str
    port_id: int
    product_number: str
    serial_number: str
    trans_type: str

class Transceivers(BaseModel):
    transceiver_list: List[Transceiver]

    @classmethod
    def from_api(cls, api_client: PyAosSwitchClient) -> 'Transceivers':
        transceiver_elements = cls.get_transceivers(api_client)
        return cls(transceiver_list=transceiver_elements)

    @classmethod
    def get_transceivers(cls, api_client: PyAosSwitchClient) -> List[dict]:
        '''
        Get transiervers on switch
        '''
        return api_client.get('transceivers')['transceiver_element']

class Interface(BaseModel)    :
    uri: str
    id: str
    name: Optional[str]
    is_port_enabled: bool
    is_port_up: bool
    config_mode: str
    trunk_mode: str
    lacp_status: str
    trunk_group: str
    is_flow_control_enabled: bool
    is_dsnoop_port_trusted: bool

class Interfaces(BaseModel):
    interfaces_list: List[Interface]
    @classmethod
    def from_api(cls, api_client: PyAosSwitchClient) -> 'Interfaces':
        ports = cls.get_interfaces(api_client)
        interfaces_list = [Interface(**entry) for entry in ports]
        return cls(interfaces_list=interfaces_list)

    @classmethod
    def get_interfaces(cls, api_client: PyAosSwitchClient):
        '''
        Get interfaces on switch
        '''

        return api_client.get('ports')['port_element']