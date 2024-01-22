from pyarubaswitch_workflows.get_port_info import export_portvlans_from_switches

YAML_FILE = 'vars.yaml'
OUTPUT_FOLDER = 'output'


def main():
    """
    Export all vlan data to csv. csv-file named after switch-hostname.
    """
    # TODO: fixa min lama errorhandling som är non-existent
    export_portvlans_from_switches(vars_file=YAML_FILE, csv_folder=OUTPUT_FOLDER)


if __name__ == '__main__':
    main()
