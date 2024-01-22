"""
Get port auth settings.


Sample output form endpoint: /mac-authentication/port

{'authorized_vlan_id': 0,
'cached_reauth_period': 0,
'is_mac_authentication_enabled': False,
'logoff_period': 300,
'mac_address_limit': 1,
'port_id': 'C2',
'quiet_period': 60,
'reauth_period': 0,
'reauthenticate': False,
'server_timeout': 300,
'unauthorized_vlan_id': 0,
'uri': '/mac-authentication/port/C2'},
{'authorized_vlan_id': 0,
'cached_reauth_period': 0,
'is_mac_authentication_enabled': True,
'logoff_period': 300,
'mac_address_limit': 1,
'port_id': 'C3',
'quiet_period': 30,
'reauth_period': 0,
'reauthenticate': False,
'server_timeout': 300,
'unauthorized_vlan_id': 0,
'uri': '/mac-authentication/port/C3'},



Sample output from endpoint: 'dot1x/authenticator'

{'authorized_vlan_id': 0,
'cached_reauth_period': 0,
'client_limit': 0,
'control': 'DAPC_AUTO',
'enforce_cache_reauth': False,
'is_authenticator_enabled': False,
'logoff_period': 300,
'max_requests': 2,
'port_id': 'C2',
'quiet_period': 60,
'reauth_period': 0,
'server_timeout': 300,
'supplicant_timeout': 30,
'tx_period': 30,
'unauth_period': 0,
'unauthorized_vlan_id': 0,
'uri': '/dot1x/authenticator/C2'},
{'authorized_vlan_id': 0,
'cached_reauth_period': 0,
'client_limit': 1,
'control': 'DAPC_AUTO',
'enforce_cache_reauth': False,
'is_authenticator_enabled': True,
'logoff_period': 300,
'max_requests': 2,
'port_id': 'C3',
'quiet_period': 20,
'reauth_period': 0,
'server_timeout': 300,
'supplicant_timeout': 30,
'tx_period': 30,
'unauth_period': 0,
'unauthorized_vlan_id': 0,
'uri': '/dot1x/authenticator/C3'},

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
        Set ports to list.
        """
        dot1x_json = self.get_dot1x_json_data()
        macauth_json = self.get_macauth_json_data()
        vlan_json = self.get_vlan_json_Data()
        self.port_list = []
        for entry in dot1x_json:
            port_id = entry['port_id']
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
        for entry in vlan_json_data:
            if (
                entry['port_id'] == port_id
                and entry['port_mode'] == 'POM_TAGGED_STATIC'
            ):
                return entry['vlan_id']

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
