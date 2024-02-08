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

import pytest

from pyarubaswitch import PyAosSwitch
from pyarubaswitch.config_reader import ConfigReader
from pyarubaswitch.logger import get_logger
from pyarubaswitch.system_status import SystemStatus

CONFIG = ConfigReader('vars.yaml')
SWITCH_IP = '192.168.119.250'

logger = get_logger(log_level='INFO')


@pytest.fixture(scope='module')
def client_fixture() -> PyAosSwitch:
    """
    Test fixture for api-client.
    """
    client = CONFIG.get_apiclient_from_file(ip_addr=SWITCH_IP)
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
    assert isinstance(client_fixture, PyAosSwitch)


def test_get_systemstatus(client_fixture):
    """
    Test getting system status.
    """
    system_status = SystemStatus.from_api(api_client=client_fixture)
    logger.info(system_status)
    assert isinstance(system_status, SystemStatus)
