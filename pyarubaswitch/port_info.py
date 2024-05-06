from typing import List, Optional

from pydantic import BaseModel

from .pyaos_switch_client import PyAosSwitchClient


class Port(BaseModel):
    port_id: str
    dot1x_enabled: Optional[bool] = None
    macauth_enabled: Optional[bool] = None
    untagged: Optional[int] = None
    tagged: Optional[List[int]] = None
    trunk_group: Optional[str] = None
    lacp_status: Optional[str] = None

class PortStats(BaseModel):
    id: str
    name: str
    packets_tx: int
    packets_rx: int
    bytes_tx: int
    bytes_rx: int
    throughput_tx_bps: int
    throughput_rx_bps: int
    error_tx: int
    error_rx: int
    drop_tx: int
    port_speed_mbps: int

class PortStatistics(BaseModel):
    port_list: List[PortStats]
    @classmethod
    def from_api(cls, api_client: PyAosSwitchClient) -> List[PortStats]:
        port_elements = cls.get_port_statistics(api_client)
        port_list = [PortStats(**entry) for entry in port_elements]
        return cls(port_list=port_list)
    
    @classmethod
    def get_port_statistics(cls,api_client:PyAosSwitchClient) -> 'PortStatistics':
        return api_client.get('port-statistics')['port_statistics_element']

class PortInfo(BaseModel):
    port_list: List[Port]

    @classmethod
    def from_api(cls, api_client: PyAosSwitchClient) -> 'PortInfo':
        port_elements = cls.get_port_data(api_client)
        return cls(port_list=port_elements)

    @classmethod
    def get_port_data(cls, api_client: PyAosSwitchClient) -> List[Port]:
        port_elements = []
        ports = cls.get_ports_jsondata(api_client)
        dot1x_json = cls.get_dot1x_json_data(api_client)
        macauth_json = cls.get_macauth_json_data(api_client)
        vlan_json = cls.get_vlan_json_data(api_client)
        for entry in ports:
            port_id = entry['id']
            port_elements.append(
                Port(
                    port_id=port_id,
                    dot1x_enabled=cls.get_dot1x_enabled(port_id, dot1x_json),
                    macauth_enabled=cls.get_macauth_enabled(port_id, macauth_json),
                    untagged=cls.get_untagged_vlan(port_id, vlan_json),
                    tagged=cls.get_tagged_vlans(port_id, vlan_json),
                    trunk_group=entry.get('trunk_group'),
                    lacp_status=entry.get('lacp_status'),
                )
            )

        return port_elements

    @classmethod
    def get_ports_jsondata(cls, api_client: PyAosSwitchClient) -> List[dict]:
        return api_client.get('ports')['port_element']

    @classmethod
    def get_dot1x_json_data(cls, api_client: PyAosSwitchClient) -> List[dict]:
        return api_client.get('dot1x/authenticator')['dot1x_authenticator_port_element']

    @classmethod
    def get_macauth_json_data(cls, api_client: PyAosSwitchClient) -> List[dict]:
        return api_client.get('mac-authentication/port')[
            'mac_authentication_port_element'
        ]

    @classmethod
    def get_vlan_json_data(cls, api_client: PyAosSwitchClient) -> List[dict]:
        vlan_json = api_client.get('vlans-ports')['vlan_port_element']
        return vlan_json

    @classmethod
    def get_dot1x_enabled(cls, port_id: str, dot1x_json: List[dict]) -> Optional[bool]:
        for entry in dot1x_json:
            if entry['port_id'] == port_id and entry['is_authenticator_enabled']:
                return True
        return False

    @classmethod
    def get_macauth_enabled(
        cls, port_id: str, macauth_json: List[dict]
    ) -> Optional[bool]:
        for entry in macauth_json:
            if entry['port_id'] == port_id and entry['is_mac_authentication_enabled']:
                return True
        return False

    @classmethod
    def get_untagged_vlan(
        cls, port_id: str, vlan_json_data: List[dict]
    ) -> Optional[int]:
        for entry in vlan_json_data:
            if entry['port_id'] == port_id and entry['port_mode'] == 'POM_UNTAGGED':
                return entry['vlan_id']
        return None

    @classmethod
    def get_tagged_vlans(
        cls, port_id: str, vlan_json_data: List[dict]
    ) -> Optional[List[int]]:
        tagged_vlans = []
        for entry in vlan_json_data:
            if (
                entry['port_id'] == port_id
                and entry['port_mode'] == 'POM_TAGGED_STATIC'
            ):
                tagged_vlans.append(entry['vlan_id'])
        return tagged_vlans if tagged_vlans else None
