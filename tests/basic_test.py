# pip install pytest
# kör sedan pytest som kommando (ej "python pytest")

'''
pytest                                                                 ✔  central_env   14:51:34  ▓▒░
===================================================================== test session starts ======================================================================
platform linux -- Python 3.8.10, pytest-7.0.0, pluggy-1.0.0
rootdir: /home/federov/python/arubacentral
collected 9 items

tests/pyarcentral_test.py .........                                                                                                                      [100%]

====================================================================== 9 passed in 9.04s =======================================================================                                                                                                                                                                                                                                                             
'''
#               
# pytest will run all files of the form test_*.py or *_test.py in the current directory and its subdirectories. More generally, it follows standard test discovery rules.    
# https://docs.pytest.org/en/6.2.x/

from pyarubaswitch.config_reader import ConfigReader

def test_print():
    assert 1 == 1
    print("hellow")


def test_get_client_from_file():
    client = ConfigReader('vars.yaml').get_apiclient_from_file("192.168.119.250")

    client.login()
    print(client.get_lldp_info_sorted())
    client.logout()