
class SntpInfo(object):

    def __init__(self, api_client):
        self.api_client = api_client

    def get_sntp_info(self):
        jsondata = self.api_client.get("system/sntp_server")

        if not self.api_client.error:
            sntp_servers = []

            for server in jsondata["sntp_servers"]:
                server_obj = SntpServer(
                    server["sntp_server_address"]["octets"], server["sntp_server_priority"])

                sntp_servers.append(server_obj)

            return sntp_servers
        elif self.api_client.error:
            print(self.api_client.error)


class SntpServer(object):

    def __repr__(self):
        return f"address: {self.address}, prio: {self.prio}"

    def __init__(self, address, prio):
        self.address = address
        self.prio = prio
