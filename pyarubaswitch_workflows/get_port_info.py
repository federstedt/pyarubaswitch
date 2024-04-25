import csv
from typing import List

from pyarubaswitch.config_reader import ConfigReader
from pyarubaswitch.exeptions import (
    ArubaApiError,
    ArubaApiLoginError,
    ArubaApiLogoutError,
    ArubaApiTimeOut,
)
from pyarubaswitch.models import VlanPort
from pyarubaswitch.pyaos_switch_client import PyAosSwitchClient

from .filehandling import models_to_csv


def get_port_vlans(api_client: PyAosSwitchClient) -> List[VlanPort]:
    """
    Get vlan info from switch ports.
    """
    api_client.login()
    port_data = api_client.get_vlan_ports()
    return port_data


def get_port_auth(api_client: PyAosSwitchClient):
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


def get_status_and_portinfo(api_client: PyAosSwitchClient):
    """
    Get system status and port info from switch.
    """
    switch_info = api_client.get_system_status()
    port_info = api_client.get_ports_info()

    return switch_info, port_info.port_list


def export_data_to_csv(csv_folder: str, switch_info, port_info):
    """ """
    csv_filename = str(csv_folder) + '/' + str(switch_info.name) + '.csv'
    port_export_csv(csv_filename, port_info)


def export_portvlans_from_switches(vars_file: str, csv_folder: str):
    """
    Get all port vlan data from all switches in list and export to one CSV.

    Use yaml vars file.
    """
    sw_timeouts = []
    sw_failed = []
    config = ConfigReader(vars_file)
    for switch in config.switches:
        try:
            client = config.get_apiclient_from_file(ip_addr=switch)
            client.login()
        except ArubaApiLoginError as exc:
            try:
                client.set_rest_version()
                client.login()
            except Exception as exc:
                print(f'Login to switch failed: {switch}')
                sw_failed.append(switch)

        if switch not in sw_failed:
            try:
                switch_info, port_info = get_status_and_portinfo(api_client=client)
                export_data_to_csv(
                    csv_folder=csv_folder, switch_info=switch_info, port_info=port_info
                )
            except ArubaApiTimeOut as exc:
                print(f'Request timeout to switch: {switch}')
                sw_timeouts.append(switch)
                sw_failed.append(switch)
            except ArubaApiError as exc:
                print(f'Error in retry of switch. {switch}')
                sw_failed.append(switch)
            finally:
                try:
                    client.logout()
                except ArubaApiLogoutError as exc:
                    pass

    print(f'Switches that timed out:\n {sw_timeouts}')
    print(f'Failed getting data from switches:\n {sw_failed}')
