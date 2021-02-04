

from pyarubaswitch.api_engine import APIuser


class LoopProtect(APIuser):

    def get_protected_ports(self):
        jsondata = self.api_client.get("loop_protect/ports")
        if self.api_passed == False:
            self.api_client.logout()

        ports = []

        for port in jsondata["loop_protect_port_element"]:

            if port["is_loop_protection_enabled"] == True:
                ports.append(port["port_id"])

        return ports
