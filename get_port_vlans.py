from pyarubaswitch.config_reader import ConfigReader
from pprint import pprint

def main():
   client = ConfigReader('vars.yaml').get_apiclient_from_file("192.168.119.250", verbose=True)

   client.login()
   system_status = client.get_system_status()
   port_data = client.get_vlans()
   pprint(port_data)
   client.logout()


if __name__ == "__main__":
    main()