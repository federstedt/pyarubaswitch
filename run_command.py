from pprint import pprint

from pyarubaswitch.aruba_switch_client import ArubaSwitchClient
from pyarubaswitch.config_reader import ConfigReader

ENDPOINT = 'dot1x/authenticator'
#'monitoring/port-access/clients'


def cli_command(sw_client, command: str) -> dict:
    """
    RUN cli command at switch.

    args:
        command(str): Command to run.
    """
    endpoint = 'cli'
    # TODO: har inte implementerat post, testa i labb.
    sw_client.api_client.post()


def main():
    config = ConfigReader('vars.yaml')
    for switch in config.switches:
        client = config.get_apiclient_from_file(ip_addr=switch)

        try:
            client.login()
            json_data = client.api_client.get(sub_url=ENDPOINT)
            pprint(json_data)
        finally:
            client.logout()


if __name__ == '__main__':
    main()


"""
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
