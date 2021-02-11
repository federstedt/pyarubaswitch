class TestClass(object):

    def __init__(self, apiclient):
        self.api_client = apiclient

    def test_get(self):
        api_get = self.api_client.get("loop_protect/portss")
        # if self.api_client.error:
        #    print(f"error in function: {self.api_client.error}")
        #    self.api_client.logout()
        if not self.api_client.error:
            return api_get
        elif self.api_client.error:
            print(self.api_client.error)
