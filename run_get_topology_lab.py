from pyarubaswitch_workflows.get_topology import TopologyMapper


# TODO: förbättra unmaneg listan, ifall netdevices innehåller en mgmt ip som inte är listad i yaml bör den hamna i unmanaged även om den svarar på lldp ?
# TODO: Fixa så man kan kolla senast aktiva portar , sen reboot eller datum. kolla om det finns färdigt i REST eller om man måste hitta på något eget.
# SNYGGA TILL SCRIPTET EXPORT GÖR FÖR MYCKET I EN FUNKTION
# TODO: Gör separata funktione som kan bli kallade själva. tex hitta bara fulswitchar, lista bara grannar , lista bara klienter mac-table, visa "aktiva" portar sen datum / uppstart
# Snygga till output och optimera för bättre läsbarhet.
# flask sida med DB ! med export knapp till csv + html + pdf 

def main():
    print("Lets go!")
    # via yaml
    run = TopologyMapper(config_filepath="vars.yaml", exlude_vlans=2, verbose=True, SSL=True, rest_version=8)

    topology = run.get_topology()
    
    run.export_topology_csv(topology_list=topology)
  



if __name__ == "__main__":
    main()
