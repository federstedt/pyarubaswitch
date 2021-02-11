
class TelnetInfo(object):

    def __init__(self, api_client):
        self.api_client = api_client

    def get_telnet_status(self):
        jsondata = self.api_client.get('telnet/server')

        if not self.api_client.error:
            return jsondata['is_telnet_server_enabled']
