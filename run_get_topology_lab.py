from pyarubaswitch_workflows.get_topology import TopologyMapper


def main():
    print("Lets go!")
    # via yaml
    run = TopologyMapper(config_filepath="vars.yaml", verbose=True, SSL=True, rest_version=8)

    topology = run.get_topology()
    
    run.export_topology_csv(topology_list=topology)
  



if __name__ == "__main__":
    main()
