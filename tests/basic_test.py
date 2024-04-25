# pip install pytest
# kör sedan pytest som kommando (ej "python pytest")

"""
pytest                                                                 ✔  central_env   14:51:34  ▓▒░
===================================================================== test session starts ======================================================================
platform linux -- Python 3.8.10, pytest-7.0.0, pluggy-1.0.0
rootdir: /home/federov/python/arubacentral
collected 9 items

tests/pyarcentral_test.py .........                                                                                                                      [100%]

====================================================================== 9 passed in 9.04s =======================================================================                                                                                                                                                                                                                                                             
"""
#
# pytest will run all files of the form test_*.py or *_test.py in the current directory and its subdirectories. More generally, it follows standard test discovery rules.
# https://docs.pytest.org/en/6.2.x/
from typing import List

import pytest

from pyarubaswitch.config_reader import ConfigReader
from pyarubaswitch.logger import get_logger
from pyarubaswitch.mac_table import MacAddressTable, MacTableElement
from pyarubaswitch.port_info import Port, PortInfo
from pyarubaswitch.pyaos_switch_client import PyAosSwitchClient
from pyarubaswitch.system_status import SystemStatus

LOG_LEVEL = 'info'
CONFIG = ConfigReader('vars.yaml')
SWITCH_IP = '192.168.119.250'

test_logger = get_logger(log_level=LOG_LEVEL, name=__name__)


@pytest.fixture(scope='module')
def client_fixture() -> PyAosSwitchClient:
    """
    Test fixture for api-client.
    """
    client = CONFIG.get_apiclient_from_file(ip_addr=SWITCH_IP)
    client.log_level = LOG_LEVEL
    yield client
    # Do teardowns etc below after tests are finished
    clear_test_data()
    client.logout()


def clear_test_data():
    """
    Remove data created by tests
    """
    pass


def test_get_client_from_file(client_fixture):
    """
    Get api-client from file and login to the switch.
    """
    client_fixture.login()
    assert isinstance(client_fixture, PyAosSwitchClient)


def test_get_systemstatus(client_fixture):
    """
    Test getting system status.
    """
    system_status = client_fixture.get_system_status()
    test_logger.debug(system_status)
    assert isinstance(system_status, SystemStatus)


def test_get_mac_table(client_fixture):
    """
    Test getting mac-address table.
    """
    mac_table = client_fixture.get_mac_table()
    test_logger.debug('mac_table: %s', mac_table)
    assert isinstance(mac_table, MacAddressTable)
    assert isinstance(mac_table.entries[0], MacTableElement)


def test_get_ports_info(client_fixture):
    """
    Test getting port info from switch.
    Contains vlan info, dot1x_auth, mac_auth, lacp settings.
    """
    port_info = client_fixture.get_ports_info()
    test_logger.debug('port-info: %s', port_info)
    assert isinstance(port_info, PortInfo)

    for port in port_info.port_list:
        assert isinstance(port, Port)
        assert isinstance(port.port_id, str)
        assert port.untagged is None or isinstance(port.untagged, int)
        assert port.tagged is None or isinstance(port.tagged, List)
        if isinstance(port.tagged, list):
            for tag_vlan in port.tagged:
                assert isinstance(tag_vlan, int)
        assert port.lacp_status is None or isinstance(port.lacp_status, str)
        assert port.trunk_group is None or isinstance(port.trunk_group, str)
