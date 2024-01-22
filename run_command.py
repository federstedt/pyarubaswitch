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



