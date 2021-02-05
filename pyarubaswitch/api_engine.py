# Session based Aruba Switch REST-API client

# TODO: hur hantera version av API , just nu hårdkodat v4 till objectet api

# TODO: se över SSL options på samtliga api-ställen. Nu är default = False och timeout=10
# TODO: fixa så man kan läsa in ssl-options i Runner manuellt via args eller yaml-fil

# TODO: justera timeout, satte till 10 i test syfte nu då jag får många timeouts på 5.

# TODO: config_reader mer error output.
# TODO: validera configen i config reader bättre
# TODO: validera korrekt input i input_parser bättre
# TODO: göm / gör password input hemlig med getpass ? https://docs.python.org/3/library/getpass.html


# TODO: pysetup: requirements pyaml , requests

# TODO: mer error output i funktioner ?


import requests
import json

# ignore ssl cert warnings (for labs)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PyAosSwitch(object):

    def __init__(self, ip_addr, username, password, SSL=False, verbose=False, timeout=10, validate_ssl=False, rest_version=7):
        '''ArubaOS-Switch API client. '''
        if SSL:
            self.protocol = 'https'
        else:
            self.protocol = 'http'

        self.session = None
        self.ip_addr = ip_addr
        self.verbose = verbose
        self.timeout = timeout
        # set to Exeption if there is a error with getting version or login
        self.error = None
        self.validate_ssl = validate_ssl
        # set rest-api version
        self.version = "v" + str(rest_version)

        self.cookie = None
        self.api_url = f'{self.protocol}://{self.ip_addr}/rest/{self.version}/'
        self.username = username
        self.password = password

        if self.verbose:
            print(f"Settings:")
            print(
                f"protcol: {self.protocol} , validate-sslcert: {self.validate_ssl}")
            print(f"timeout: {self.timeout}, api-version: {self.version}")
            print(f"api-url: {self.api_url}")

    def login(self):
        '''Login to switch with username and password, get token. Return token '''
        if self.session == None:
            self.session = requests.session()
        url = self.api_url + "login-sessions"
        login_data = {"userName": self.username, "password": self.password}
        if self.verbose:
            print(f'Logging into: {url}, with: {login_data}')

        try:
            r = self.session.post(url, data=json.dumps(
                login_data), timeout=self.timeout, verify=self.validate_ssl)
            r.raise_for_status()
        except Exception as e:
            if self.error == None:
                self.error = {}
            self.error['login_error'] = e

    def logout(self):
        '''Logout from the switch. Using token from login function. Makes sure switch doesn't run out of sessions.'''
        if self.session == None:
            print("No session need to login first, before you can logout")
        else:
            try:
                logout = self.session.delete(
                    self.api_url + "login-sessions", timeout=self.timeout)
                logout.raise_for_status()
                self.session.close()
            except Exception as e:
                if self.error == None:
                    self.error = {}
                self.error["logout_error"] = e

    def get(self, sub_url):
        '''GET requests to the API. uses base-url + incoming-url call. Uses token from login function.'''
        return self.invoke("GET", sub_url)

    def put(self):
        '''PUT requests to API. Uses base-url + incoming-url with incoming data to set. NOT ACTIVE YET!'''
        pass

    def invoke(self, method, sub_url):
        '''Invokes specified method on API url. GET/PUT/POST/DELETE etc.
            Returns json response '''
        if self.session == None:
            self.login()

        url = self.api_url + sub_url
        try:
            r = self.session.request(
                method, url, timeout=self.timeout, verify=self.validate_ssl)
            r.raise_for_status()
            json_response = r.json()
            return(json_response)
        except Exception as e:
            print(e)
            self.logout()
            self.session.close()
            exit(1)


class APIuser(object):
    '''Base class for APIusage objects. Contains all the stuff a API-worker needs to get it's data 
    from the SwitchClient. Can be passed an API-client object OR login information to be used for getting data. '''

    def __init__(self, switch_ip=None, username=None, password=None, apiclient=None, SSL=False, verbose=False, timeout=10, validate_ssl=False):

        if (switch_ip == None or username == None or password == None) and apiclient == None:
            print("Error! you must either pass along login details or a apiclient object")
            exit(0)
        if apiclient == None:
            self.switch_ip = switch_ip
            self.username = username
            self.password = password
            self.SSL = SSL
            self.timeout = timeout
            self.verbose = verbose
            self.validate_ssl = validate_ssl
            self.api_client = PyAosSwitch(
                switch_ip, self.username, self.password, SSL=self.SSL, verbose=self.verbose, timeout=self.timeout, validate_ssl=self.validate_ssl)
            self.api_passed = False
        else:
            self.api_client = apiclient
            self.api_passed = True
