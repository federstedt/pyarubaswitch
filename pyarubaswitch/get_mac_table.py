# Get mac-address table

class MacAddressTable(object):

    def __init__(self, api_client):
        self.api_client = api_client


    def get_mac_table(self):
        jsondata = self.api_client.get("mac-table")

        if not self.api_client.error:
            if self.api_client.legacy_api == False:
                mac_table_entry_elements = jsondata["mac_table_entry_element"]
            else:
                mac_table_entry_elements = jsondata["mac-table"]
            mac_address_table = []
            for x in mac_table_entry_elements:
                mac_addr = MacTableElement(x["mac_address"],x["port_id"],x["vlan_id"])
                mac_address_table.append(mac_addr)
            
            return mac_address_table



class MacTableElement(object):

    def __repr__(self):
        return f"mac_address: {self.mac_address}, port_id: {self.port_id}, vlan_id: {self.vlan_id}"

    def __init__(self, mac_address, port_id, vlan_id):
        self.mac_address = mac_address
        self.port_id = port_id
        self.vlan_id = vlan_id