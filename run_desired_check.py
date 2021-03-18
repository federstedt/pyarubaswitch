#!/usr/bin/python3
from argparse import ArgumentParser

from pyarubaswitch_workflows.check_desired_vlans import PortChecker

parser = ArgumentParser()

parser.add_argument("--switchip", "-sw", help="switch-ipaddress")
parser.add_argument("--username", "-u" ,help="username for switch")
parser.add_argument("--password", "-p" ,help="password for switch")
parser.add_argument("--SSL", "-s", help="True/False for using SSL in API-calls")
parser.add_argument("--verbose", "-v", help="True/False for verbosemode")
parser.add_argument("--untagged","-n",help="Desired untagged vlan")
parser.add_argument("--tagged","-t", help="Desired tagged vlans")
parser.add_argument("--devicetype","-d", help="type of neighbour device to check port vlans for. ap/switch .")

args = parser.parse_args()

def main():
    print(f"Comparing desired vlans to actual vlans on {args.devicetype} port")
    
    # convert to list delimit with , and remove spaces
    switch_string = args.switchip
    switch_string = switch_string.replace(" ", "")
    switches = switch_string.split(",")

    untag = []
    untag.append(args.untagged)

    tagged_string = args.tagged
    tagged_string = tagged_string.replace(" ", "")
    tag = tagged_string.split(",")

        

    if args.verbose:
        print(f"Desired untag: {untag}")
        print(f"Desired tagged {tag}")
    port_check = PortChecker(untag, tag, devicetype=args.devicetype, arg_username=args.username,arg_password=args.password,arg_switches=switches,SSL=args.SSL)
    port_check.check_switches()

if __name__ == "__main__":
    main()