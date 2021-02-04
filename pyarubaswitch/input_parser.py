# return valid credentials from input by user, to be used if yaml file is not used

class InputParser(object):

    def __init__(self):
        print("Input details to continue...")
        self.username = input("username: ")
        self.password = input("password: ")
        switch_string = input("ip-addresses (comma seperated): ")
        # remove spaces from switch ip-address input.
        switch_string = switch_string.replace(" ", "")
        self.switches = switch_string.split(",")
