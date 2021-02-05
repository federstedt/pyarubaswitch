# read desired vlan untag + tag
# get switch or AP neighbour, check those ports for desired compare to actual

# TODO: make desired_checker check so that list contains ints and NOT strings

from pyarubaswitch.common_ops import shorten_numberlist
from pyarubaswitch.aruba_switch_client import ArubaSwitchClient
from workflows.runner import Runner


class PortChecker(Runner):

    def __init__(self, desired_untag, desired_tag, config_filepath=None, arg_username=None, arg_password=None,
                 arg_switches=None, SSL=False, verbose=False, timeout=10, validate_ssl=False):

        self.desired_untag = desired_untag
        self.desired_tag = desired_tag
        super(PortChecker, self).__init__(config_filepath,
                                          arg_username, arg_password, arg_switches,
                                          SSL, verbose, timeout, validate_ssl)

    def check_switches(self):
        for switch in self.switches:
            if self.verbose == True:
                print(f"Getting info from {switch}")
            switch_run = ArubaSwitchClient(
                switch, self.username, self.password, self.SSL, self.verbose, self.timeout, self.validate_ssl, self.rest_version)
            if self.verbose == True:
                print("logging in...")
            switch_run.api_client.login()

            lldp_aps = switch_run.get_lldp_aps()

            lldp_switches = switch_run.get_lldp_switches()

            for ap in lldp_aps:
                ap_port_data = switch_run.get_port_vlan(ap.local_port)
                print(f"{ap.name}")
                print(f"actual vlans: {ap_port_data}")
                ap_miss_untag, ap_miss_tag = ap_port_data.check_desired_vlans(
                    self.desired_untag, self.desired_tag)
                print(
                    f"missing vlans: untag {ap_miss_untag}, tag: {ap_miss_tag} ")
            for sw in lldp_switches:
                switch_port_data = switch_run.get_port_vlan(sw.local_port)
                print(sw.name)
                print(f"actual vlans: {switch_port_data}")
                sw_miss_untag, sw_miss_tag = switch_port_data.check_desired_vlans(
                    self.desired_untag, self.desired_tag)
                print(
                    f"missing vlans:  untag: {sw_miss_untag}, tag: {sw_miss_tag}")

            switch_run.api_client.logout()
