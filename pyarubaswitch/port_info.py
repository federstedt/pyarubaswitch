from typing import List, Optional

from pydantic import BaseModel

from .pyaos_switch_client import PyAosSwitchClient


class Port(BaseModel):
    port_id: str
    untagged: Optional[int] = None
    tagged: Optional[List[int]] = None
    dot1x_enabled: Optional[bool] = None
    macauth_enabled: Optional[bool] = None
    lacp_status: Optional[str] = None
    trunk_group: Optional[str] = None


class VlanPort(Port):
    missing_untagged: Optional[List[int]] = []
    missing_tagged: Optional[List[int]] = []

    def check_desired_vlans(self, desired_untag, desired_tag):
        """Returns missing vlans that are defined as desired untag/tag"""
        for vlan in desired_untag:
            if vlan not in self.untagged:
                self.missing_untagged.append(vlan)
        for vlan in desired_tag:
            if vlan not in self.tagged:
                self.missing_tagged.append(vlan)

        return self.missing_untagged, self.missing_tagged


class PortInfo(BaseModel):
    _port_list: List[Port] = []  # Use a private attribute to store port_list

    @classmethod
    def from_api(cls, api_client: PyAosSwitchClient) -> 'PortInfo':
        port_info = cls()
        port_info.port_list = port_info.get_port_data(api_client)
        return port_info

    def get_port_data(self, api_client: PyAosSwitchClient):
        ports = self.get_ports_jsondata(api_client)
        dot1x_json = self.get_dot1x_json_data(api_client)
        macauth_json = self.get_macauth_json_data(api_client)
        vlan_json = self.get_vlan_json_data(api_client)

        # list containing all ports and their info
        portdata_list = []
        for entry in ports:
            port_id = entry['id']
            portdata_list.append(
                Port(
                    port_id=port_id,
                    dot1x_enabled=self.dot1x_enabled(port_id, dot1x_json=dot1x_json),
                    macauth_enabled=self.macauth_enabled(
                        port_id, macauth_json=macauth_json
                    ),
                    untagged=self.vlan_untagged(
                        port_id=port_id, vlan_json_data=vlan_json
                    ),
                    tagged=self.vlan_tagged(port_id=port_id, vlan_json_data=vlan_json),
                    trunk_group=entry['trunk_group'],
                )
            )
        # Update port_list using the setter method
        return portdata_list

    # Define the property getter and setter for port_list
    @property
    def port_list(self):
        return self._port_list

    @port_list.setter
    def port_list(self, value):
        self._port_list = value

    # Define the remaining methods as before
    def get_ports_jsondata(self, api_client: PyAosSwitchClient) -> List[dict]:
        data = api_client.get('ports')
        return data['port_element']

    def get_dot1x_json_data(self, api_client: PyAosSwitchClient) -> List[dict]:
        data = api_client.get('dot1x/authenticator')['dot1x_authenticator_port_element']
        return data

    def get_macauth_json_data(self, api_client: PyAosSwitchClient) -> List[dict]:
        data = api_client.get('mac-authentication/port')[
            'mac_authentication_port_element'
        ]
        return data

    def get_vlan_json_data(self, api_client: PyAosSwitchClient) -> List[dict]:
        data = api_client.get('vlans-ports')['vlan_port_element']
        return data

    def vlan_untagged(self, port_id: str, vlan_json_data: List[dict]) -> Optional[int]:
        for entry in vlan_json_data:
            if entry['port_id'] == port_id and entry['port_mode'] == 'POM_UNTAGGED':
                return entry['vlan_id']

    def vlan_tagged(
        self, port_id: str, vlan_json_data: List[dict]
    ) -> Optional[List[int]]:
        tagged_vlans = []
        for entry in vlan_json_data:
            if (
                entry['port_id'] == port_id
                and entry['port_mode'] == 'POM_TAGGED_STATIC'
            ):
                tagged_vlans.append(entry['vlan_id'])

        if tagged_vlans:
            return tagged_vlans

    def dot1x_enabled(self, port_id: str, dot1x_json: List[dict]) -> bool:
        for entry in dot1x_json:
            if (
                entry['port_id'] == port_id
                and entry['is_authenticator_enabled'] is True
            ):
                return True
        return False

    def macauth_enabled(self, port_id: str, macauth_json: List[dict]) -> bool:
        for entry in macauth_json:
            if (
                entry['port_id'] == port_id
                and entry['is_mac_authentication_enabled'] is True
            ):
                return True
        return False
