"""
Exception raised by Radarly's client.
"""


class RateReached(Exception):
    """Error raised when the user can not make any more request."""
    def __init__(self, message):
        super().__init__(message)
        self.radarly_message = message


class AuthenticationError(Exception):
    """Error raised if (client_id, client_secret) doesn't match any
    credentials in our database.
    """
    def __init__(self, error_type):
        self.type = error_type

    def __str__(self):
        if self.type == 'invalid_client':
            return 'The client_id or the client_secret is invalid.'
        elif self.type == 'invalid_scope':
            return ("The asked scopes are uncompatible with the scopes "
                    "linked to your account.")
        elif self.type == 'unsupported_grant_type':
            return "The grant_type is not currently supported."
        return 'Uncategorized Error.'


class NoInitializedApi(Exception):
    """Error raised if the module could not find an API to make a request"""
    def __str__(self):
        return (
            'No API has been initialized.'
        )
