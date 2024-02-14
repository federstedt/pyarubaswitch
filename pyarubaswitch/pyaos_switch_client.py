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


import json

import requests

# ignore ssl cert warnings (for labs)
import urllib3

from .exeptions import (
    APIClientError,
    ArubaApiError,
    ArubaApiLoginError,
    ArubaApiTimeOut,
)
from .logger import get_logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PyAosSwitchClient(object):
    def __init__(
        self,
        ip_addr,
        username,
        password,
        SSL=False,
        verbose=False,
        timeout=5,
        validate_ssl=False,
        rest_version=7,
    ):
        """ArubaOS-Switch API client."""

        self.session = None
        self.__ip_addr = ip_addr
        self.verbose = verbose
        self.timeout = timeout
        # set to Exeption if there is a error with getting version or login
        self.error = None
        self.__ssl = SSL
        self.validate_ssl = validate_ssl
        # set rest-api version
        self.rest_verion_int = rest_version
        self.version = 'v' + str(rest_version)
        if rest_version < 4:
            self.legacy_api = True
        else:
            self.legacy_api = False

        self.cookie = None

        self.username = username
        self.password = password

        self.__log_level = 'warning'

        if self.verbose:
            print(f'Settings:')
            print(f'protcol: {self.protocol} , validate-sslcert: {self.validate_ssl}')
            print(f'timeout: {self.timeout}, api-version: {self.version}')
            print(f'api-url: {self.api_url}')

    @property
    def log_level(self):
        """
        Returns:
            String representing log_level of logger.
        """
        return self.__log_level

    @log_level.setter
    def log_level(self, level):
        """
        Setter method of log_level.

        Args:
            level(str): String representing a logging level.
        """
        if isinstance(level, str):
            self.__log_level = level
        else:
            raise APIClientError('logging level provided is not a string.')

    @property
    def logger(self):
        """
        logging.Logger object.
        """
        return get_logger(self.log_level)

    @property
    def protocol(self):
        """
        Protocol for REST communicaitons.
        Either http or https.

        Based on SSL=True or False.
        """
        if self.__ssl:
            return 'https'
        else:
            return 'http'

    @property
    def ip_addr(self):
        """
        IP-Address of switch.
        """
        return self.__ip_addr

    @ip_addr.setter
    def ip_addr(self, value):
        """
        Set IP-Address of the switch.

        value(str): Ip-address in string format.
        """
        self.__ip_addr = value

    @property
    def api_url(self):
        return f'{self.protocol}://{self.ip_addr}/rest/{self.version}/'

    def login(self):
        """Login to switch with username and password, get token. Return token"""
        if self.session == None:
            self.session = requests.session()
        url = self.api_url + 'login-sessions'
        login_data = {'userName': self.username, 'password': self.password}
        if self.verbose:
            print(f'Logging into: {url}, with: {login_data}')

        try:
            r = self.session.post(
                url,
                data=json.dumps(login_data),
                timeout=self.timeout,
                verify=self.validate_ssl,
            )
            r.raise_for_status()

            if r.status_code == 201:
                json_resp = r.json()
                if self.verbose:
                    print(f'login success! url: {url}')
                    print('login data:')
                    print(json_resp)
                if self.legacy_api:
                    self.cookie = json_resp['cookie']
            else:
                print('Error login:')
                print(r.status_code)
                if self.error == None:
                    self.error = {}
                    self.error['login_error'] = r
        except requests.exceptions.Timeout as exc:
            raise ArubaApiLoginError(408, 'Request has timed out.') from exc
        except requests.HTTPError as exc:
            raise ArubaApiLoginError(
                status_code=exc.response.status_code,
                message=f'{str(r.json())}',
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise ArubaApiLoginError(500, str(exc)) from exc

    def logout(self):
        """Logout from the switch. Using token from login function. Makes sure switch doesn't run out of sessions."""
        if self.session == None:
            print('No session need to login first, before you can logout')
        else:
            if self.legacy_api:
                headers = {'cookie': self.cookie}
            else:
                headers = None
            try:
                logout = self.session.delete(
                    self.api_url + 'login-sessions',
                    timeout=self.timeout,
                    headers=headers,
                )
                logout.raise_for_status()
                self.session.close()
                if self.verbose:
                    print('Logged out successfully')
            except Exception as e:
                if self.error == None:
                    self.error = {}
                self.error['logout_error'] = e

    def get_rest_version(self):
        """GET switch RESTAPI version and return as string ie "7"
        :return version latest supportert RESTversion in string format.
        """
        if self.session is None:
            self.login()
        url = f'{self.protocol}://{self.ip_addr}/rest/version'

        if self.verbose:
            print(f'Getting rest-api version from url: {url}')

        if self.legacy_api:
            headers = {'cookie': self.cookie}
        else:
            headers = None

        r = self.session.get(
            url, timeout=self.timeout, verify=self.validate_ssl, headers=headers
        )
        r.raise_for_status()

        if r.status_code == 200:
            json_resp = r.json()

            if self.verbose:
                print('rest-version data:')
                print(json_resp)
            return json_resp
        else:
            print(f'Error getting rest version from {url}')
            print(r)

    def set_rest_version(self):
        """
        Gets API latest supported apiversion from switch and uses that version for all future calls.
        """
        versions = self.get_rest_version()
        if versions:
            latest_ver = versions['version_element'][-1]['version']
            # remove .X from v1.0

            split_string = latest_ver.split('.', 1)
            latest_ver = split_string[0]
            # set self.api_version to latest supported
            self.version = latest_ver
            # refresh api url with latest version
            self.set_api_url()

            # remove v , convert to int
            self.rest_verion_int = int(latest_ver.replace('v', ''))
            # > ver7 not equals legacy logins without session cookie
            if self.rest_verion_int > 6:
                self.legacy_api = False
            elif self.rest_verion_int < 6:
                self.legacy_api = True
        else:
            print('Error getting switch version')

    def get(self, sub_url):
        """GET requests to the API. uses base-url + incoming-url call. Uses token from login function."""
        return self.invoke('GET', sub_url)

    def post(self):
        """PUT requests to API. Uses base-url + incoming-url with incoming data to set. NOT ACTIVE YET!"""
        pass

    def invoke(self, method, sub_url):
        """Invokes specified method on API url. GET/PUT/POST/DELETE etc.
        Returns json response"""
        if self.session is None:
            self.login()

        url = self.api_url + sub_url
        if self.legacy_api:
            headers = {'cookie': self.cookie}
        else:
            headers = None
        try:
            if self.verbose:
                print(f'Calling API url: {url}, headers: {headers} method: {method}')
            r = self.session.request(
                method,
                url,
                timeout=self.timeout,
                verify=self.validate_ssl,
                headers=headers,
            )
            r.raise_for_status()
            json_response = r.json()
            return json_response
        except requests.exceptions.Timeout as exc:
            raise ArubaApiTimeOut(408, 'Request has timed out.') from exc
        except requests.HTTPError as exc:
            raise ArubaApiError(
                status_code=exc.response.status_code,
                message=f'{str(r.json())} , using: {method} , header {headers}',
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise ArubaApiError(500, str(exc)) from exc

    #### Higher level functions for getting specific endpoints.
    def get_system_status(self):
        """Retrieve system status using SystemStatus classmethod.

        Returns:
            SystemStatus object.
        """
        from .system_status import SystemStatus  # Deferred import

        return SystemStatus.from_api(self)

    def get_mac_table(self):
        """
        Get mac-address table from switch using classmethod.

        Returns:
            MacAddressTable object containing MacTableElement.
        """
        from .mac_table import MacAddressTable

        return MacAddressTable.from_api(self)

    def get_ports_info(self):
        """
        Get PortInfo from all switchports.

        Returns:
            PortInfo(list of Port objects)
        """
        from .port_info import PortInfo

        return PortInfo.from_api(self)
