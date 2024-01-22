"""
Get port settings.
"""
from typing import List

from .exeptions import ArubaPortError
from .models import Port


class PortInfo:
    """
    Auth and vlan config info from ports on switch.
    """

    def __init__(self, api_client) -> None:
        self.api_client = api_client
        self.port_list = []

    def get_ports_jsondata(self) -> dict:
        """
        Get all ports.
        """
        data = self.api_client.get('ports')
        return data['port_element']

    def get_dot1x_json_data(self) -> dict:
        """
        Returns all ports dot1x settings.
        """
        data = self.api_client.get('dot1x/authenticator')[
            'dot1x_authenticator_port_element'
        ]
        return data

    def get_macauth_json_data(self) -> dict:
        """
        Returns all ports macauth settings.
        """
        data = self.api_client.get('mac-authentication/port')[
            'mac_authentication_port_element'
        ]
        return data

    def get_vlan_json_Data(self) -> dict:
        """
        Vlans ports data.
        """
        data = self.api_client.get('vlans-ports')['vlan_port_element']
        return data

    def set_port_list(self):
        """
        set ports list. Add data from ports, dot1x, macauth and vlan-ports.
        """
        ports = self.get_ports_jsondata()
        dot1x_json = self.get_dot1x_json_data()
        macauth_json = self.get_macauth_json_data()
        vlan_json = self.get_vlan_json_Data()

        self.port_list = []
        for entry in ports:
            port_id = entry['id']
            self.port_list.append(
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

    def vlan_untagged(self, port_id: str, vlan_json_data: List[dict]) -> int:
        """
        Get untagged vlan on port_id.
        """
        for entry in vlan_json_data:
            if entry['port_id'] == port_id and entry['port_mode'] == 'POM_UNTAGGED':
                return entry['vlan_id']

    def vlan_tagged(self, port_id: str, vlan_json_data: List[dict]) -> List:
        """
        Get tagged vlan on port_id.
        """
        tagged_vlans = []
        for entry in vlan_json_data:
            if (
                entry['port_id'] == port_id
                and entry['port_mode'] == 'POM_TAGGED_STATIC'
            ):
                tagged_vlans.append(entry['vlan_id'])

        if len(tagged_vlans) > 0:
            return tagged_vlans
        # elif len(tagged_vlans) == 1:
        #     return tagged_vlans  # [0]

    def dot1x_enabled(self, port_id: str, dot1x_json: List[dict]) -> bool:
        """
        Args:
            port_id(str): port_id to check.
        Returns:
            True if port is dotx_enabled.
        """
        for entry in dot1x_json:
            if entry['port_id'] == port_id:
                if entry['is_authenticator_enabled'] is True:
                    return True
        return False

    def macauth_enabled(self, port_id: str, macauth_json: List[dict]) -> bool:
        """
        Args:
            port_id(str): port_id to check.
        Returns:
            True if port is macuath is enabled.
        """
        for entry in macauth_json:
            if entry['port_id'] == port_id:
                if entry['is_mac_authentication_enabled'] is True:
                    return True
        return False
