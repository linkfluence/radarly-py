"""
Exception raised by Radarly's client.
"""


class RateReached(Exception):
    """Error raised when the user can not make any more request."""
    def __init__(self, message):
        super().__init__(message)
        self.radarly_message = message


class BadAuthentication(Exception):
    """Error raised if (client_id, client_secret) doesn't match any
    credentials in our database.
    """
    def __str__(self):
        return 'The client_id or the client_secret is invalid.'


class NoInitializedApi(Exception):
    """Error raised if the module could not find an API to make a request"""
    def __str__(self):
        return (
            'No API has been initialized.'
        )
