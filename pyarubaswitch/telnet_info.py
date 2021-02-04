from pyarubaswitch.api_engine import APIuser

# TODO: skall denna returnera ett objekt ??? naaah ?


class TelnetInfo(APIuser):

    def get_telnet_status(self):
        jsondata = self.api_client.get('telnet/server')
        if self.api_passed == False:
            self.api_client.logout()

        return jsondata['is_telnet_server_enabled']
