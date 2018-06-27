"""
Exception raised by the client.
"""

from requests.exceptions import HTTPError

from .utils.misc import dict_to_tsv


class NoInitializedApi(Exception):
    """Error raised if the module could not find an API to make a request"""
    def __str__(self):
        return (
            'No API has been initialized.'
        )


class AuthenticationError(Exception):
    """Error raised if (client_id, client_secret) doesn't match any
    credential in our database.
    """
    def __init__(self, error_type):
        super().__init__()
        self.type = error_type

    def __str__(self):
        if self.type == 'invalid_client':
            return 'The client_id or the client_secret is invalid.'
        elif self.type == 'invalid_scope':
            return ("The asked scopes are uncompatible with the scopes "
                    "linked to your account.")
        elif self.type == 'unsupported_grant_type':
            return "The grant_type is not currently supported."
        elif self.type == 'unauthorized_client':
            return "You don't have the permission to access the API."
        return 'Error: {}'.format(self.type)


class RadarlyHTTPError(HTTPError):
    """An HTTP error occured when querying Radarly's API"""
    def __str__(self):
        data = {
            'Code': self.response.status_code,
            'Reason': self.response.reason,
            'URL': self.response.url,
            'Content': self.response.text or '(no content)',
        }
        if 400 <= data['Code'] < 500:
            data['Reason'] += ' (Client Side Error)'
        elif 500 <= data['Code'] < 600:
            data['Reason'] += ' (Servor Side Error)'
        return '{}\n{}'.format(
            'An error occured during the request.', dict_to_tsv(data)
        )


class RateReached(Exception):
    """Error raised when the user can not a request anymore."""
    def __init__(self, message):
        super().__init__(message)
        self.radarly_message = message


class PublicationUpdateFailed(Exception):
    """Error raised if the update of a publication's field failed."""
    def __init__(self, fields):
        super().__init__()
        self.fields = fields

    def __str__(self):
        return ("The field `{}` of the publication "
                "has not been updated.").format(
                    ", ".join(self.fields)
                )
