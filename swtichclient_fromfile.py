from pyarubaswitch.config_reader import ConfigReader


def main():
   client = ConfigReader('vars.yaml').get_apiclient_from_file("192.168.119.250", verbose=True)

   client.login()
   system_status = client.get_system_status()
   print(system_status)
   client.logout()


if __name__ == "__main__":
    main()