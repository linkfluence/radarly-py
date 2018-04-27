"""
Authentification class used by ``requests`` on each request. The authentication
system used by Radarly is based on a Bearer Token system.
"""

from requests.auth import AuthBase


class RadarlyAuth(AuthBase): # pylint: disable=R0903
    """Authorization object used by request to acccess Radarly's API.
    This object is automatically initialized by the ``RadarlyApi`` object
    using your access_token so you don't need to handle the authentication
    for each of your requests to the API. If you want to do some other requests
    using requests module without using the client python, you can use this
    object for authentication.

    >>> import requests
    >>> from radarly.auth import RadarlyAuth
    >>> auth = RadarlyAuth(<my_access_token>)
    >>> url_user = 'https://radarly.linkfluence.com/1.O/user.json'
    >>> requests.get(url_user, auth=auth)
    """
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer {.token}'.format(self)
        return r

    def __repr__(self):
        token = self.token[:20] + '...'
        return '<RadarlyAuth.token={}.type=bearer>'.format(token)