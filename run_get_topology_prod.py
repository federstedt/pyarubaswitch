from pyarubaswitch_workflows.get_topology import TopologyMapper


#TODO: fixa när klienter är på trunkar, de är också dubletter men verkar inte träffa bort-sorterings-regelen
# TODO: hitta fulswitchar / omanagerade switchar som ej är med i ip-listan
# TODO: förbättra unmaneg listan, ifall netdevices innehåller en mgmt ip som inte är listad i yaml bör den hamna i unmanaged även om den svarar på lldp ?
# TODO:
# SNYGGA TILL SCRIPTET EXPORT GÖR FÖR MYCKET I EN FUNKTION
# Snygga till output och optimera för bättre läsbarhet.
# Exportera till pdf eller ritning , något roligare än csv ?

def main():
    print("Lets go!")
    # old switches pre rest-version 7 are very slow over ssl.
    run = TopologyMapper(config_filepath="prod_vars.yaml",exlude_vlans=203, verbose=True, SSL=False, rest_version=2, timeout=40)

    topology = run.get_topology()
    
    run.export_topology_csv(topology_list=topology)
  



if __name__ == "__main__":
    main()
