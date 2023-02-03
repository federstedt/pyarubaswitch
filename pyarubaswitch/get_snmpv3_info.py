
from .models import Snmpv3

class Snmpv3Info(object):

    def __init__(self, api_client):
        self.api_client = api_client

    def get_snmpv3_info(self):
        jsondata = self.api_client.get('snmpv3')

        if not self.api_client.error:
            snmpv3_info = Snmpv3(jsondata["is_snmpv3_server_enabled"],
                                 jsondata["is_non_snmpv3_access_readonly"], jsondata["is_snmpv3_messages_only"])

            return snmpv3_info
        elif self.api_client.error:
            print(self.api_client.error)



