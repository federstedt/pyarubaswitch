from pyarubaswitch_workflows.get_topology import TopologyMapper


def main():
    print("Lets go!")
    # via yaml
    run = TopologyMapper("vars.yaml", verbose=True, SSL=True, rest_version=2)

    topology = run.get_topology()
    
    run.export_topology_csv("export/labb_env", topology_list=topology)
  



if __name__ == "__main__":
    main()
