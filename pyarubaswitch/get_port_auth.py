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


class PortAuthInfo:
    """
    Auth config info from ports on switch
    """

    def __init__(self, api_client) -> None:
        self.api_client = api_client
        self.ports = []

    @property
    def dot1x_json_data(self) -> dict:
        """
        Returns all ports dot1x settings.
        """
        data = self.api_client.get('dot1x/authenticator')
        return data

    @property
    def macauth_json_data(self) -> dict:
        """
        Returns all ports macauth settings.
        """
        return self.api_client.get('mac-authentication/port')

    def set_ports(self):
        """
        Set ports to list.
        """
        if self.dot1x_json_data is not None:
            for element in self.dot1x_json_data:
                port_id = element['port_id']
                self.ports.append(
                    Port(
                        port_id=port_id,
                        dot1x_enabled=self.dot1x_enabled(port_id),
                        macauth_enabled=self.macauth_enabled(port_id),
                    )
                )
        else:
            raise ArubaPortError(
                'Could not check if dot1x is enabled on port. No dot1x_json_data found.'
            )

    def dot1x_enabled(self, port_id: str) -> bool:
        """
        Args:
            port_id(str): port_id to check.
        Returns:
            True if port is dotx_enabled.
        """
        if self.dot1x_json_data is not None:
            for element in self.dot1x_json_data:
                if element['port_id'] == port_id:
                    if element['is_authenticator_enabled'] is True:
                        return True
            return False
        else:
            raise ArubaPortError(
                'Could not check if dot1x is enabled on port. No dot1x_json_data found.'
            )

    def macauth_enabled(self, port_id: str) -> bool:
        """
        Args:
            port_id(str): port_id to check.
        Returns:
            True if port is macuath is enabled.
        """
        if self.macauth_json_data is not None:
            for element in self.macauth_json_data:
                if element['port_id'] == port_id:
                    if element['is_mac_authentication_enabled'] is True:
                        return True
            return False
        else:
            raise ArubaPortError(
                'Could not check if macauth is enabled on port. No macauth_json_data found.'
            )
