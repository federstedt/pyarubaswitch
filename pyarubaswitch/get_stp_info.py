
class StpInfo(object):

    def __init__(self, api_client):
        self.api_client = api_client

    def get_stp_info(self):
        jsondata = self.api_client.get('stp!!')

        if not self.api_client.error:
            stp_info = STP(jsondata["is_enabled"],
                           jsondata["priority"], jsondata["mode"])

            return stp_info


class STP(object):

    def __repr__(self):
        return f"enabled: {self.enabled}, prio: {self.prio}, mode: {self.mode}"

    def __init__(self, enabled, prio, mode):
        self.enabled = enabled
        self.prio = prio
        self.mode = mode
