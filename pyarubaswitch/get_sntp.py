from pyarubaswitch.api_engine import APIuser


class SntpInfo(APIuser):

    def get_sntp_info(self):
        jsondata = self.api_client.get("system/sntp_server")
        if self.api_passed == False:
            self.api_client.logout()

        sntp_servers = []

        for server in jsondata["sntp_servers"]:
            server_obj = SntpServer(
                server["sntp_server_address"]["octets"], server["sntp_server_priority"])

            sntp_servers.append(server_obj)

        return sntp_servers


class SntpServer(object):

    def __repr__(self):
        return f"address: {self.address}, prio: {self.prio}"

    def __init__(self, address, prio):
        self.address = address
        self.prio = prio
