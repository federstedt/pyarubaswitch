# baseinfo getter
from workflows.runner import Runner
from pyarubaswitch.common_ops import shorten_numberlist
from pyarubaswitch.aruba_switch_client import ArubaSwitchClient


class BaseInfoGetter(Runner):

    def get_info(self):
        for switch in self.switches:
            if self.verbose == True:
                print(f"Getting info from {switch}")
            switch_run = ArubaSwitchClient(
                switch, self.username, self.password, self.SSL, self.verbose, self.timeout, self.validate_ssl, self.rest_version)
            if self.verbose == True:
                print("logging in...")
            switch_run.api_client.login()

            if self.verbose:
                print("Getting system info")
            system_status = switch_run.get_system_status()
            print(system_status)

            if self.verbose:
                print("Getting telnet-server status")
            telnet_status = switch_run.get_telnet_server_status()
            print(telnet_status)

            if self.verbose:
                print("Getting STP info")
            stp_info = switch_run.get_stp_info()

            print(stp_info)

            if self.verbose:
                print("Getting snmpv3 info")
            snmpv3_info = switch_run.get_snmpv3()
            print(snmpv3_info)

            if self.verbose:
                print("Getting sntp-servers")
            sntp_info = switch_run.get_sntp()
            print(sntp_info)

            loop_pports = switch_run.get_loop_protected_ports()
            if not switch_run.api_client.error:
                if self.verbose:
                    print("Getting loop-protected ports")
                # makes the list shorter with 1,2,3,5,6 -> 1-3,5-6
                loop_pports = shorten_numberlist(loop_pports)
                print(loop_pports)

            if self.verbose:
                print("Getting unprotected ports")
            un_loop_ports = switch_run.get_non_loop_protected_ports()

            if not switch_run.api_client:
                un_loop_ports = shorten_numberlist(un_loop_ports)
                print(un_loop_ports)

            if self.verbose:
                print("Getting lldp based info")
            self.get_lldp_info(switch_run)

            if self.verbose == True:
                print("logging out...")
            switch_run.api_client.logout()

            if switch_run.api_client.error:
                print(f"There was an error:\n {switch_run.api_client.error}")

    def get_lldp_info(self, api_runner):
        if self.verbose == True:
            print("getting lldp-aps")

        lldp_aps = api_runner.get_lldp_aps()
        print(lldp_aps)

        if self.verbose == True:
            print("getting lldp-switches")

        lldp_switches = api_runner.get_lldp_switches()
        print(lldp_switches)
        if not api_runner.api_client.error:
            if self.verbose == True:
                print("getting vlans on Access point ports, and switchports")

            for ap in lldp_aps:
                ap_port_data = api_runner.get_port_vlan(ap.local_port)
                print(f"{ap.name}")
                print(ap_port_data)
            for sw in lldp_switches:
                switch_port_data = api_runner.get_port_vlan(sw.local_port)
                print(sw.name)
                print(switch_port_data)
