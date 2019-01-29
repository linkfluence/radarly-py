User
~~~~

Get Current User information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method allows users to retrieve current user information and in particular,
the list of available projects.


**Request**
   ``GET`` https://radarly.linkfluence.com/1.1/users.json
**Headers**
   * *Authorization*: Bearer XXX


**Structure of the response**::

    {
        "id":              <int>,    # user id
        "name":            <str>, # user name
        "email":           <str>, # user email
        "theme":           <str>, # user background customization: "dark" or "light"
        "locale":          <str>, # user locale (UI language): "en_GB" or "fr_FR" or "de_DE"
        "timezone":        <str>, # user timezone: eg. "Europe/Paris"
        "projects":[
            {
                "id":      <int>,    # project id
                "label":   <str>  # project label
            },
            ...
        ]
    }


**Use Case Example**:

.. http:example:: curl wget python-requests
   :request: ./user/request.get-current-user-infos.txt
   :response: ./user/response.get-current-user-infos.txt
