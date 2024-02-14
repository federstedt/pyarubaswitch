from typing import List, Optional

from pydantic import BaseModel

from .pyaos_switch_client import PyAosSwitchClient


class MacTableElement(BaseModel):
    mac_address: str
    port_id: str
    vlan_id: int


class MacAddressTable(BaseModel):
    entries: List[MacTableElement]

    @classmethod
    def from_api(cls, api_client: PyAosSwitchClient) -> 'MacAddressTable':
        json_data = api_client.get('mac-table')
        mac_table_entry_elements = []

        if api_client.rest_verion_int > 2 and 'mac_table_entry_element' in json_data:
            mac_table_entry_elements = json_data['mac_table_entry_element']
        else:
            api_client.logger.info(
                'mac_table_entry_element not found in json dict. Old API-version ?'
            )
            mac_table_entry_elements = json_data.get('mac_table', [])

        entries = [
            MacTableElement(
                mac_address=entry.get('mac_address'),
                port_id=entry.get('port_id'),
                vlan_id=entry.get('vlan_id'),
            )
            for entry in mac_table_entry_elements
        ]

        return cls(entries=entries)
