from .models import STP


class StpInfo(object):

    def __init__(self, api_client):
        self.api_client = api_client

    def get_stp_info(self):
        jsondata = self.api_client.get('stp')

        if jsondata:
            stp_info = STP(enabled=jsondata["is_enabled"],
                           prio=jsondata["priority"], mode=jsondata["mode"])

            return stp_info
        
        return None



