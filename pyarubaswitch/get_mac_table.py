# Get mac-address table
from .models import MacTableElement

class MacAddressTable(object):

    def __init__(self, api_client):
        self.api_client = api_client


    def get_mac_table(self):
        jsondata = self.api_client.get("mac-table")

        if not self.api_client.error:
            if self.api_client.rest_verion_int > 2 and 'mac_table_entry_element' in jsondata:
                mac_table_entry_elements = jsondata["mac_table_entry_element"]
            else:
                print(f'ERROR: mac_table_entry_element not found')
                print(jsondata)
                mac_table_entry_elements = jsondata["mac_table"]
            mac_address_table = []
            for x in mac_table_entry_elements:
                mac_addr = MacTableElement(x["mac_address"],x["port_id"],x["vlan_id"])
                mac_address_table.append(mac_addr)
            
            return mac_address_table



