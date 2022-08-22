from pyarubaswitch_workflows.runner import Runner
from pyarubaswitch_workflows.filehandling import CsvExporter

from pprint import pprint

def main():
    print("Lets go!")
    # old switches pre rest-version 7 are very slow over ssl.
    run = Runner(config_filepath="prod_vars.yaml", verbose=True, SSL=False, rest_version=7, timeout=40)

    switches = run.get_transceivers()

    pprint(switches)
    exporter = CsvExporter(switches)
    exporter.export_transceivers_csv("transceivers.csv")

    
   
if __name__ == "__main__":
    main()