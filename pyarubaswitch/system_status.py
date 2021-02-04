# get system status information
from pyarubaswitch.api_engine import APIuser


class SystemStatus(APIuser):

    def get_system_info(self):
        sys_json = self.api_client.get('system/status')
        # if api_session was created within the object itself. Logout as it will not be reused outside this object
        if self.api_passed == False:
            self.api_client.logout()

        sysinfo = SystemInfo(sys_json["name"], sys_json['hardware_revision'],
                             sys_json['firmware_version'], sys_json['serial_number'])

        return sysinfo


class SystemInfo(object):

    def __repr__(self):
        return f"name: {self.name}, hw: {self.hw_rev}, fw: {self.fw_ver}, sn: {self.serial}"

    def __init__(self, name, hw_rev, fw_ver, sn):
        self.name = name
        self.hw_rev = hw_rev
        self.fw_ver = fw_ver
        self.serial = sn
