class APIClientError(Exception):
    """
    Generic error from the client.
    """

    pass


class ArubaApiError(Exception):
    """
    Error from API endpoint communications
    """

    def __init__(self, status_code, message) -> None:
        self.status_code = status_code
        self.message = message


class ArubaApiLoginError(ArubaApiError):
    """
    Error loging in to switch.
    """

    pass


class ArubaApiTimeOut(Exception):
    """
    Timout calling API endpoint.
    """

    pass


class ArubaPortError(Exception):
    """
    Error parsing port data.
    """

    pass
