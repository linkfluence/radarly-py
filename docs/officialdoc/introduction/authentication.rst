Authenticate with the OAuth 2.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Authentification is available via OAuth 2.0. The OAuth layer of Radarly is
based on the official specification. We support two flows:

* Client Credentials Grant
* Authorization Code Grant



Do you need to authenticate ?
-----------------------------
The Radarly API requires authentication - specifically requests made on
behalf of a user. Authenticated requests require an access token. These
tokens are unique to a user and should be stored securely. Access tokens
may have an expiration date.



Client Authentication (for confidential client only)
----------------------------------------------------
If the client type is confidential, the client and authorization server
establish a client authentication method suitable for the security requirements
of the authorization server. There are two options to establish this
authentification needed for the /token endpoint:

* Including the client credentials in the request-body.
* Using the HTTP Basic authentication scheme (with the client_id as username
  and client_secret as password).



Receiving an access token through ‘Client Credentials Grant’
------------------------------------------------------------

.. warning:: The host for this request differs from the habitual path of
    the API. You must use: https://oauth.linkfluence.com/


**Request**
   ``POST`` /oauth2/token
**Headers**
   * *Content-Type*: ``application/x-www-form-urlencoded``
**Post data parameters**
   * *client_id*: (string)
   * *client_secret*: (string)
   * *scope* (optional, string) - List of scopes delimited by a space:
     ``‘listening historical-data’``
   * *grant_type*: ``client_credentials``


.. http:example:: curl wget python-requests
    :request: ./requests/request.authentication.txt
    :response: ./requests/response.authentication.txt


Receiving an access token through ‘Authorization Code Grant’
------------------------------------------------------------

.. warning:: The root path for this request differs from the habitual
    path of the API. You must use: https://oauth.linkfluence.com/

In order to receive an access token, you must do the following:

1. Direct the user to our authorization url (
   ``https://oauth.linkfluence.com/oauth2/authorize?state=xxx&redirect_uri=xxx&client_id=xxx&response_type=code``
   ). If the user is not logged in, they will be asked to log in. The user
   will be asked if they would like to grant your application access to her
   Radarly data
2. The server will redirect the user to a URI of your choice. Take the
   provided code parameter and exchange it for an access token by
   POSTing the code to our access_token endpoint.


**Request**
   ``POST`` https://oauth.linkfluence.com/oauth2/token
**Headers**
   * *Content-Type*: ``application/x-www-form-urlencoded``
**Post data parameters**
   * *code* (string)
   * *client_id* (string)
   * *client_secret* (optional, string) Only for confidential client
   * *state* (string)
   * *redirect_uri* (string)
   * *grant_type* : ``authorization_code``


Example:

.. http:example:: curl wget python-requests
    :request: ./requests/request.authorization.txt
    :response: ./requests/response.authorization.txt


Refreshing an access token
--------------------------

.. warning:: The root path for this request differs from the habitual path of
    the API. You must use: https://oauth.linkfluence.com/


**Request**
   ``POST`` https://oauth.linkfluence.com/oauth2/token
**Headers**
   * *Content-Type*: ``application/x-www-form-urlencoded``
**Post data parameters**
   * *refresh_token*: <REFRESH_TOKEN>
   * *grant_type*: ``refresh_token``
   * *client_id*: (optional, string): Only for confidential client
   * *client_secret*: (optional, string): Only for confidential client

.. http:example:: curl wget python-requests
    :request: ./requests/request.refresh.txt
    :response: ./requests/response.refresh.txt


Miscellaneous
-------------

**Login Permissions (Scopes)**
The OAuth 2.0 specification allows you to specify the scope of the access you
are requesting from the user. All approved apps have a basic access by default,
but if you plan on asking for extended access such as reading data from social
networks as posts or reviewss, you will need to specify these scopes in your
authorization request. Note that in order to use these extended permissions,
you must first contact us to generate a client. Here are the scopes we
currently support:

*listening*
    to read data from social networks as posts, reviews, images…
*social-performance*
    to read personal information about registered social network account
    in Radarly.
*historical-data*
    to read historical data from social networks as posts, reviews, images…

You should only request the scope you need at the time of authorization.
If in the future you require additional scope, you may direct the user to
the authorization URL with that additional scope to be granted. If you
attempt to perform a request with an access token that is not authorized
for that scope, you will receive a response with status 401 Unauthorized.

To request multiple scopes at once, simply separate the scopes by a space
(eg. ``scope="listening social-performance"``)

**Access protected resources**
To access any protected resource you will need to include a valid access
token in your request. You must provide the token in the HTTP header
``Authorization``:

.. http:example:: curl wget python-requests
    :request: ./requests/request.example.txt
    :response: ./requests/response.example.txt

**How to find my client credentials**
If you want to use our api, and be able to request an access token you
first need to contact us to generate an appropriate token to your use case.
A token validity duration depends on the generated client.
