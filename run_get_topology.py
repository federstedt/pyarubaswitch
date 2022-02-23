from pyarubaswitch_workflows.get_topology import TopologyMapper
from pprint import pprint

def main():
    print("Lets go!")
    # via yaml
    run_1 = TopologyMapper("vars.yaml", verbose=True, SSL=True)
    # with args

    # with input

    mac_table = run_1.get_mac_table()
    pprint(mac_table)


if __name__ == "__main__":
    main()
