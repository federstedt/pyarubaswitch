# get vlans for specified port
from typing import List

from .models import VlanPort


class Vlaninfo(object):
    def __init__(self, api_client):
        self.api_client = api_client

    @property
    def vlan_json_data(self) -> dict:
        """returns port objects with vlan info."""
        vlan_info = self.api_client.get("vlans-ports")

        return vlan_info

    @property
    def vlan_data(self) -> List[VlanPort]:
        """
        Vlan data in readable format.

        Returns:
            List[Port]: List of port objects.
        """
        ports = []
        if self.vlan_json_data is not None:
            for element in self.vlan_json_data["vlan_port_element"]:
                untagged_vlan = None
                tagged_vlan = None
                if element["port_mode"] == "POM_UNTAGGED":
                    untagged_vlan = element["vlan_id"]
                elif element["port_mode"] == "POM_TAGGED_STATIC":
                    tagged_vlan = element["vlan_id"]

                port = VlanPort(
                    port_id=element["port_id"],
                    untagged=untagged_vlan,
                    tagged=tagged_vlan,
                )
                ports.append(port)

        return ports

    def port_vlans(self, port: int) -> VlanPort:
        """
        Returns:
            Port info.
        """
        if self.vlan_data is not None:
            for entry in self.vlan_data:
                if entry.port_id == port:
                    return entry
