from pyarubaswitch_workflows.get_topology import TopologyMapper


def main():
    print("Lets go!")
    # old switches pre rest-version 7 are very slow over ssl.
    run = TopologyMapper("prod_vars.yaml", verbose=True, SSL=False, rest_version=2, timeout=40)

    topology = run.get_topology()
    
    run.export_topology_csv("export/artro", topology_list=topology)
  



if __name__ == "__main__":
    main()
