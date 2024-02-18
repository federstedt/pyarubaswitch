# Session based Aruba Switch REST-API client
import json

import requests

# ignore ssl cert warnings (for labs)
import urllib3

from .exeptions import (
    APIClientError,
    ArubaApiError,
    ArubaApiLoginError,
    ArubaApiLogoutError,
    ArubaApiTimeOut,
)
from .logger import get_logger

# ignore ssl cert warnings (for labs)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PyAosSwitchClient(object):
    def __init__(
        self,
        ip_addr,
        username,
        password,
        SSL=False,
        timeout=10,
        validate_ssl=False,
        rest_version=7,
    ):
        """ArubaOS-Switch API client."""

        self.session = None
        self.__ip_addr = ip_addr
        self.timeout = timeout
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
        if self.log_level.upper() == 'DEBUG':
            self.output_settings()

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

    def output_settings(self):
        """
        Output settings to debug-logger.
        """
        self.logger.debug(
            f'API-Client Settings:\nprotcol: {self.protocol} , validate-sslcert: {self.validate_ssl}\ntimeout: {self.timeout}, api-version: {self.version}\napi-url: {self.api_url}'
        )

    def login(self):
        """
        Login to switch with username and password, get token.
        Store token in session (API-version > 5).
        If using legacy api store token in self.cookie variable.
        """
        if self.session is None:
            self.session = requests.session()
        url = self.api_url + 'login-sessions'
        login_data = {'userName': self.username, 'password': self.password}

        self.logger.debug(f'Logging into: {url}')

        try:
            response = self.session.post(
                url,
                data=json.dumps(login_data),
                timeout=self.timeout,
                verify=self.validate_ssl,
            )
            response.raise_for_status()

            if response.status_code == 201:
                json_resp = response.json()
                if self.legacy_api:
                    self.cookie = json_resp['cookie']
            else:
                raise ArubaApiLoginError(
                    status_code=response.status_code,
                    message=f'Error logging in to: {url}.\n{response}',
                )
        except requests.exceptions.Timeout as exc:
            raise ArubaApiLoginError(408, 'Request has timed out.') from exc
        except requests.HTTPError as exc:
            raise ArubaApiLoginError(
                status_code=exc.response.status_code,
                message=f'{str(response.json())}',
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise ArubaApiLoginError(500, str(exc)) from exc

    def logout(self):
        """Logout from the switch. Using token from login function. Makes sure switch doesn't run out of sessions."""
        if self.session == None:
            self.logger.info('No session need to login first, before you can logout')
        else:
            if self.legacy_api:
                headers = {'cookie': self.cookie}
            else:
                headers = None
            try:
                logout_resp = self.session.delete(
                    self.api_url + 'login-sessions',
                    timeout=self.timeout,
                    headers=headers,
                )
                logout_resp.raise_for_status()
                self.session.close()
                self.logger.debug('Logged out successfully')
            except requests.exceptions.Timeout as exc:
                raise ArubaApiLogoutError(408, 'Request has timed out.') from exc
            except requests.HTTPError as exc:
                raise ArubaApiLogoutError(
                    status_code=exc.response.status_code,
                    message=f'{str(logout_resp.json())}',
                ) from exc
            except requests.exceptions.RequestException as exc:
                raise ArubaApiLogoutError(500, str(exc)) from exc

    def get_rest_version(self):
        """
        GET switch RESTAPI versions from switch.

        Returns:
            json_resp(dict): json response from api.
        """
        if self.session is None:
            self.login()
        url = f'{self.protocol}://{self.ip_addr}/rest/version'

        self.logger.debug(f'Getting rest-api version from url: {url}')

        # TODO: can be removed ? 18/2 2024 I commented this.
        # if self.legacy_api:
        #     headers = {'cookie': self.cookie}
        # else:
        #     headers = None
        try:
            resp = self.session.get(
                url, timeout=self.timeout, verify=self.validate_ssl, headers=None
            )
            resp.raise_for_status()

            if resp.status_code == 200:
                json_resp = resp.json()
                self.logger.debug('rest-version data:%s', json_resp)
                return json_resp
            else:
                raise ArubaApiError(status_code=resp.status_code, message=resp)
        except requests.exceptions.Timeout as exc:
            raise ArubaApiTimeOut(408, 'Request has timed out.') from exc
        except requests.HTTPError as exc:
            raise ArubaApiError(
                status_code=exc.response.status_code,
                message=f'{str(resp.json())}',
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise ArubaApiError(500, str(exc)) from exc

    def set_rest_version(self):
        """
        Get API latest supported apiversion from switch and uses that version for all future calls.
        Sets version to self.rest_version variable in 'v7' format, and to self.rest_version_int in integer format.
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
            raise APIClientError(
                f'Error getting API-version from switch. Cannot parse: {versions}'
            )

    def get(self, sub_url):
        """GET requests to the API. uses base-url + incoming-url call. Uses token from login function."""
        return self.invoke('GET', sub_url)

    def post(self):
        """PUT requests to API. Uses base-url + incoming-url with incoming data to set. NOT IMPLEMENTED YET!"""
        pass

    def invoke(self, method, sub_url):
        """Invokes specified method on API url. GET/PUT/POST/DELETE etc.

        Returns:
            json_response(dict): json response from API.
        """
        if self.session is None:
            self.login()

        url = self.api_url + sub_url
        if self.legacy_api:
            headers = {'cookie': self.cookie}
        else:
            headers = None
        try:
            self.logger.debug(f'Calling API url: {url}, method: {method}')
            response = self.session.request(
                method,
                url,
                timeout=self.timeout,
                verify=self.validate_ssl,
                headers=headers,
            )
            response.raise_for_status()
            json_response = response.json()
            return json_response
        except requests.exceptions.Timeout as exc:
            raise ArubaApiTimeOut(408, 'Request has timed out.') from exc
        except requests.HTTPError as exc:
            raise ArubaApiError(
                status_code=exc.response.status_code,
                message=f'{str(response.json())} , using: {method} , header {headers}',
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise ArubaApiError(500, str(exc)) from exc

    ####
    #### Higher level functions for getting specific endpoints. #####
    ####

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
