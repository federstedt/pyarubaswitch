
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


class Snmpv3(object):

    def __repr__(self):
        return f"enabled: {self.enabled}, is_non_v3_readonly: {self.non_snmpv3_readonly}, only_v3: {self.only_v3}"

    def __init__(self, enabled, readonly, only_v3):
        self.enabled = enabled
        self.non_snmpv3_readonly = readonly
        self.only_v3 = only_v3
