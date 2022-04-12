class Transceiver(object):

    def __repr__(self):
        return f"Transceiver: part_number: {self.part_number}, port_id: {self.port_id}, product_number: {self.product_number}, serial_number: {self.serial_number}, type: {self.type}" 

    def __init__(self, part_number, port_id, product_number, serial_number, trans_type):
        self.part_number = part_number
        self.port_id = port_id
        self.product_number = product_number
        self.serial_number = serial_number
        self.type = trans_type



class InterfaceInfo(object):

    def __init__(self, api_client):
        self.api_client = api_client


    def get_transceivers(self):
        '''
        Get transiervers on switch
        '''
        jsondata = self.api_client.get('transceivers')

        if not self.api_client.error:
            transceivers = []
            for entry in jsondata["transceiver_element"]:
                trans = Transceiver(part_number=entry["part_number"],port_id=entry["port_id"],product_number=entry["product_number"],serial_number=entry["serial_number"],trans_type=entry["type"])
                transceivers.append(trans)
            return transceivers
        else:
            print(self.api_client.errror)





