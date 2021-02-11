from pyarubaswitch.aruba_switch_client import ArubaSwitchClient
from pyarubaswitch.input_parser import InputParser


def main():
    config = InputParser()

    for switch in config.switches:
        client = ArubaSwitchClient(
            switch, config.username, config.password, SSL=True)
        client.login()
        client.error_test()
        if client.api_client.error:
            print(f"There was an error: {client.api_client.error}")
            print("ERROR, logging out")
            client.logout()


if __name__ == "__main__":
    main()
