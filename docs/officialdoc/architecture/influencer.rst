Influencer
~~~~~~~~~~

Get Influencer Data
^^^^^^^^^^^^^^^^^^^

This method allows users to get an influencer’s metrics and information. It sends
back the metrics and the user information, depending of the platform.

**Request**
   ``GET`` https://radarly.linkfluence.com/1.1/projects/:pid/influencer.json
**Headers**
   * *Authorization*: Bearer XXX
**Path Parameter**
   * pid (*string*): project id
**Query String**
   * iid (*string*): influencer id
   * platform (*string*): source platform


**Structure of the response**::

    {
        "metrics": <hash>,     # all the metrics depending of the platform,
        "user": <hash>,        # user information depending of the platform
    }

Example:

.. http:example:: curl wget python-requests
   :request: ./influencers/request.get-influencer-data.txt
   :response: ./influencers/response.get-influencer-data.txt


Get All Influencers
^^^^^^^^^^^^^^^^^^^

This method allows to retrieve the influencers for a set of publications.
It sends back users.

**Request**
   ``POST`` https://radarly.linkfluence.com/1.1/projects/:pid/influencers.json
**Headers**
   * *Authorization*: Bearer XXX
**Path Parameter**
   * pid: project id
**Payload Parameter**
    Standard Search Parameter + Following Parameter:

    ========= ======== =========================================================
    Parameter Type     Description
    ========= ======== =========================================================
    sortBy    string   Sorting parameter - ``volumetry`` or ``radar.impression``
                       or ``radar.reach``
    sortOrder string   Sorting order - ``desc`` or ``asc``
    start     int      Starting index (used for pagination). Defaults to 0
    limit     int      Max number of results. Defaults to 25
    ========= ======== =========================================================

Response::

    "users" : <array>,   # the list of users


Example:

.. http:example:: curl wget python-requests
   :request: ./influencers/request.get-influencers.txt
   :response: ./influencers/response.get-influencers.txt


Add an Influencer to a Corpus
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method allows to add an influencer to a corpus.

**Request**
   ``POST`` https://radarly.linkfluence.com/1.1/projects/:pid/corpora/:cid/sources.json
**Headers**
   * *Authorization*: Bearer XXX
**Path Parameter**
   * pid: project id
   * cid: corpora id
**Payload Parameter**
    ========= ======== ====================================
    Parameter Type     Description
    ========= ======== ====================================
    XXXXXX    array    List of the user under the form
                       {name:”", screenName:"", userId: ""}
    ========= ======== ====================================

**Structure of the response**::

    {
        {
            "sources":{
                "twitter":[
                    {
                        "userId":<string>,
                        "screenName":<string>,
                        "name":<string>,
                        "created":<date>
                    }
                ],
                "facebook": [],
                ...
    }


Example:

.. http:example:: curl wget python-requests
   :request: ./influencers/request.add-influencer-to-corpora.txt
   :response: ./influencers/response.add-influencer-to-corpora.txt


Set Influencer Tag
^^^^^^^^^^^^^^^^^^

This method allows users to set a tag on an influencer.

**Request**
   ``PUT`` https://radarly.linkfluence.com/1.1/projects/:pid/influencers/tags.json
**Headers**
   * *Authorization*: Bearer XXX
**Path Parameter**
   * pid (*string*): project id
**Query String**
   * iid (*string*): influencer id
   * platform (*string*): document source type
   * tags (*list*): list of existing tag names

**Structure of the response**::

    {
        "userId":"1653145898",
        "taskId":"4dca8f58-de75-41ff-aa74-4f6da760623e"
    }
