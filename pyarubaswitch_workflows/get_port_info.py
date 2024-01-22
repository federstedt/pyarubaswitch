import csv
from typing import List

from pyarubaswitch.aruba_switch_client import ArubaSwitchClient
from pyarubaswitch.config_reader import ConfigReader
from pyarubaswitch.models import VlanPort

from .filehandling import models_to_csv


def get_port_vlans(api_client: ArubaSwitchClient) -> List[VlanPort]:
    """
    Get vlan info from switch ports.
    """
    api_client.login()
    port_data = api_client.get_vlan_ports()
    return port_data


def get_port_auth(api_client: ArubaSwitchClient):
    """
    Get port auth_modes.
    """
    port_info = api_client.get_portauth_mode()
    return port_info


def port_export_csv(filename: str, port_data: List[VlanPort]):
    """
    Export port vlandata to csv.

    Args:
        filename(str): Name file to output csv-data to.
        port_data(list[Port]): List containing Port objects.
    """
    models_to_csv(
        csv_filepath=filename,
        models=port_data,
        include_fields={
            'port_id',
            'untagged',
            'tagged',
            'dot1x_enabled',
            'macauth_enabled',
            'trunk_group',
        },
        exlude_none=True,
    )


def export_portvlans_from_switches(vars_file: str, csv_folder: str):
    """
    Get all port vlan data from all switches in list and export to one CSV.

    Use yaml vars file.
    """
    config = ConfigReader(vars_file)
    for switch in config.switches:
        client = config.get_apiclient_from_file(ip_addr=switch, SSL=True)
        client.api_client.verbose = True
        try:
            switch_info = client.get_system_status()
            # vlan_info = get_port_vlans(api_client=client)
            port_info = client.get_port_info()
        finally:
            client.api_client.logout()
        csv_filename = str(csv_folder) + '/' + str(switch_info.name) + '.csv'
        port_export_csv(csv_filename, port_info)
