

class LoopProtect(object):

    def __init__(self, api_client):
        self.api_client = api_client

    def get_protected_ports(self):
        jsondata = self.api_client.get("loop_protect/ports")
        if not self.api_client.error:
            ports = []
            for port in jsondata["loop_protect_port_element"]:

                if port["is_loop_protection_enabled"] == True:
                    ports.append(port["port_id"])

            return ports

    def get_unprotected_ports(self):
        jsondata = self.api_client.get("loop_protect/ports")
        if not self.api_client.error:
            ports = []

            for port in jsondata["loop_protect_port_element"]:

                if port["is_loop_protection_enabled"] == False:
                    ports.append(port["port_id"])

            return ports
