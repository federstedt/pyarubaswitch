from pyarubaswitch_workflows.get_topology import TopologyMapper
from pprint import pprint

def main():
    print("Lets go!")
    # via yaml
    run = TopologyMapper("vars.yaml", verbose=True, SSL=True, rest_version=2)

    run.get_topology()
  



if __name__ == "__main__":
    main()
