from pydantic import BaseModel

from .pyaos_switch_client import PyAosSwitchClient


class SystemStatus(BaseModel):
    name: str
    hardware_revision: str
    firmware_version: str
    serial_number: str
    base_ethernet_address: str

    @classmethod
    def from_api(cls, api_client: PyAosSwitchClient):
        sys_status = api_client.get('system/status')
        return cls(
            name=sys_status['name'],
            hardware_revision=sys_status['hardware_revision'],
            firmware_version=sys_status['firmware_version'],
            serial_number=sys_status['serial_number'],
            base_ethernet_address=sys_status['base_ethernet_address']['octets'],
        )
