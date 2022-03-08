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

    def __init__(self, ip_addr, username, password, SSL=False, verbose=False, timeout=5, validate_ssl=False, rest_version=7):
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
        self.rest_verion_int = rest_version
        self.version = "v" + str(rest_version)
        if rest_version < 4:
            self.legacy_api = True
        else:
            self.legacy_api = False

        self.cookie = None

        self.set_api_url()

        self.username = username
        self.password = password

        if self.verbose:
            print(f"Settings:")
            print(
                f"protcol: {self.protocol} , validate-sslcert: {self.validate_ssl}")
            print(f"timeout: {self.timeout}, api-version: {self.version}")
            print(f"api-url: {self.api_url}")


    def set_api_url(self):
        self.api_url = f'{self.protocol}://{self.ip_addr}/rest/{self.version}/'

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
            
            
           
            if r.status_code == 201:
                json_resp = r.json()
                if self.verbose:
                    print(f"login success! url: {url}")
                    print("login data:")
                    print(json_resp)
                if self.legacy_api:
                    self.cookie = json_resp["cookie"]
            else:
                print("Error login:")
                print(r.status_code)
                if self.error == None:
                    self.error = {}
                    self.error['login_error'] = r


        except Exception as e:
            if self.error == None:
                self.error = {}
            self.error['login_error'] = e


    def logout(self):
        '''Logout from the switch. Using token from login function. Makes sure switch doesn't run out of sessions.'''
        if self.session == None:
            print("No session need to login first, before you can logout")
        else:
            if self.legacy_api:
                headers = {'cookie': self.cookie}
            else:
                headers = None
            try:
                logout = self.session.delete(
                    self.api_url + "login-sessions", timeout=self.timeout, headers=headers)
                logout.raise_for_status()
                self.session.close()
                if self.verbose:
                    print("Logged out successfully")
            except Exception as e:
                if self.error == None:
                    self.error = {}
                self.error["logout_error"] = e

    def get_rest_version(self):
        ''' GET switch RESTAPI version and return as string ie "7" 
        :return version latest supportert RESTversion in string format.
        '''
        if self.session == None:
            self.login()
        url = f"{self.protocol}://{self.ip_addr}/rest/version"

        if self.verbose:
            print(f"Getting rest-api version from url: {url}")

        if self.legacy_api:
                headers = {'cookie': self.cookie}
        else:
            headers = None
        try:
            r = self.session.get(url, timeout=self.timeout,verify=self.validate_ssl,headers=headers)
            r.raise_for_status()

            if r.status_code == 200:
                json_resp = r.json()

                if self.verbose:
                    print(f"rest-version data:")
                    print(json_resp)
                return(json_resp)
            else:
                print(f"Error getting rest version from {url}")
                print(r)
        
        except Exception as e:
            if self.error == None:
                self.error = {}
            self.error['version_error'] = e

    def set_rest_version(self):
        '''
        Gets API latest supported apiversion from switch and uses that version for all future calls.
        '''
        versions = self.get_rest_version()
        if versions:
            latest_ver = versions["version_element"][-1]["version"]
            #remove .X from v1.0  

            split_string = latest_ver.split(".", 1)
            latest_ver = split_string[0]
            # set self.api_version to latest supported
            self.version = latest_ver
            # refresh api url with latest version
            self.set_api_url()

            # remove v , convert to int
            self.rest_verion_int = int(latest_ver.replace("v",""))
            # > ver7 not equals legacy logins without session cookie
            if self.rest_verion_int > 6:
                self.legacy_api = False
        else:
            print("Error getting switch version")



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
        if self.legacy_api:
            headers = {'cookie': self.cookie}
        else:
            headers = None
        try:
            r = self.session.request(
                method, url, timeout=self.timeout, verify=self.validate_ssl, headers=headers)
            r.raise_for_status()
            json_response = r.json()
            return(json_response)
        except Exception as e:
            if self.error == None:
                self.error = {}
            self.error["invoke_error"] = e
            if self.verbose:
                print("ERROR FOUND:")
                print(self.error)
            #DEBUG: print(f"error in engine: {self.error}")

    def reset_error(self):
        self.error = None
