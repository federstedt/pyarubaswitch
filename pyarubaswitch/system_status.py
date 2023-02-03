from .models import SystemInfo

class SystemStatus(object):

    def __init__(self, api_client):
        self.api_client = api_client

    def get_system_info(self):
        sys_json = self.api_client.get('system/status')

        if not self.api_client.error and sys_json:

            sysinfo = SystemInfo(name = sys_json["name"], hw_rev = sys_json['hardware_revision'],
                                 fw_ver = sys_json['firmware_version'], serial= sys_json['serial_number'], mac_addr = sys_json['base_ethernet_address']['octets'])

            return sysinfo
        elif self.api_client.error:
            print(self.api_client.error)
            return None



