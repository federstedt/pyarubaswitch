
class SystemStatus(object):

    def __init__(self, api_client):
        self.api_client = api_client

    def get_system_info(self):
        sys_json = self.api_client.get('system/status')

        if not self.api_client.error:

            sysinfo = SystemInfo(sys_json["name"], sys_json['hardware_revision'],
                                 sys_json['firmware_version'], sys_json['serial_number'])

            return sysinfo
        elif self.api_client.error:
            print(self.api_client.error)


class SystemInfo(object):

    def __repr__(self):
        return f"name: {self.name}, hw: {self.hw_rev}, fw: {self.fw_ver}, sn: {self.serial}"

    def __init__(self, name, hw_rev, fw_ver, sn):
        self.name = name
        self.hw_rev = hw_rev
        self.fw_ver = fw_ver
        self.serial = sn
