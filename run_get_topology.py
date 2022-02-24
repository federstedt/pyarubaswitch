from pyarubaswitch_workflows.get_topology import TopologyMapper
from pprint import pprint

def main():
    print("Lets go!")
    # via yaml
    run_1 = TopologyMapper("vars.yaml", verbose=True, SSL=True, rest_version=2)
    # with args

    pprint(run_1.get_rest_version())
    # with input
    '''
    mac_table = run_1.get_mac_table()
    pprint(mac_table)
    for entry in mac_table:
        if entry.port_id == "9":
            print(entry.mac_address)
    '''


if __name__ == "__main__":
    main()
