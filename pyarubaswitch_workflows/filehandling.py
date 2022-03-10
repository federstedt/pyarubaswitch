import csv


class CsvExporter(object):

    def __init__(self, switches):
        self.switches = switches

    def export_transceivers_csv(self, filename):
        '''
        Exports transceivers from switch objects to csv file
        params:
        :switches list of switch objects
        : filename string, filename of csvfile
        '''
        with open(file=filename, mode="w",encoding='utf-8-sig') as f:
            writer = csv.writer(f)

            # header
            header = ["switch_ip","part_number","port_id","product_number","serial_number","type"]
            writer.writerow(header)

            for sw in self.switches:
                for trans in sw.transceivers:
                    writer.writerow([sw.switch_ip, trans.part_number, trans.port_id, trans.product_number,trans.serial_number, trans.type])

