Publication
~~~~~~~~~~~

.. Warning::
	Restriction on Document Output
	Depending to the type of the document, the list of available fields can differs. 
	The search route will always returns all the available fields. 
	The reason a field may not be available to a document are the following:
		* You are not granted to access this information. Some platforms restrict access to meta-data to the owner or to the recipient of the post.
		* The platform does not allow us in its terms of use to return all the content through our own APIs. For instance, Twitter is restricting the content to be distributed through APIs to only Tweet IDs, Direct Message IDs, and/or User IDs.
	
	To know more about the subject and to learn how to access restricted data, consider reading the :doc:`/officialdoc/architecture/documentoutput` section

Search Publications
^^^^^^^^^^^^^^^^^^^

This method allows users to search for publications.

**Request**
   ``POST`` https://radarly.linkfluence.com/1.1/projects/:pid/inbox/search.json
**Headers**
   * *Authorization*: Bearer XXX
**Path Parameter**
   * pid: project id
**Payload Parameter**
    Standard Search Parameter + Following Parameter:

    ========= ======== ===============================================================
    Parameter Type     Description
    ========= ======== ===============================================================
    metrics   array    List of the metrics returned in the statistics - Allowed
                       metrics - ``doc``, ``impression``, ``reach``, ``engagements``,
                       ``repost``.
    sortBy    string   Sorting parameter - ``volumetry`` or ``radar.impression``
                       or ``radar.reach``
    sortOrder string   Sorting order - ``desc`` or ``asc``
    start     int      Starting index (used for pagination) Defaults to 0
    limit     int      Max number of results. Defaults to 25
    ========= ======== ===============================================================


**Structure of the response**::

    {
        "hits" :           <array>,   # the list of publications
        "total" :          <int>,     # the total count of publications
    }


.. http:example:: curl wget python-requests
   :request: ./publication/request.search-for-publications.txt
   :response: ./publication/response.search-for-publications.txt


Get Metadata of a Publication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method allows users to get publication's metadata.


**Request**
   ``GET`` https://radarly.linkfluence.com/1.1/projects/:pid/documents.json
**Headers**
   * *Authorization*: Bearer XXX
**Path Parameter**
   * pid: project id
**Query String Parameter**
   * uid: document id
   * platform: document source type, ie. ``blog``, ``dailymotion``,
     ``website``, ``forum``, ``twitter``, ``media``, ``instagram``, ``gplus``,
     ``facebook``, ``linkedin``, ``youtube``, ``comment``, ``vkontakte``,
     ``youku``, ``wechat``
   * from (optional)
   * to (optional)

.. http:example:: curl wget python-requests
   :request: ./publication/request.get-publication-metadata.txt
   :response: ./publication/response.get-publication-metadata.txt


Set Document Tags
^^^^^^^^^^^^^^^^^

This method allows users to set a tag on a document. The response is a
confirmation of the new document values.

**Request**
   ``POST`` https://radarly.linkfluence.com/1.1/projects/:pid/documents.json
**Headers**
   * *Authorization*: Bearer XXX
**Path Parameter**
   * pid: project id
**Query String Parameter**
   * uid: document id
   * platform: document source type, ie. ``blog``, ``dailymotion``,
     ``website``, ``forum``, ``twitter``, ``media``, ``instagram``,
     ``gplus``, ``facebook``, ``linkedin``, ``youtube``, ``comment``,
     ``vkontakte``, ``youku``, ``wechat``


**Payload Parameter**::

    {
        "doc":{
            "<NameOfField>":"<new_value>", // to change a radar value like `tone`, `lang`, `country`,...
            "radar": {
                "tag": {
                    "custom": {
                        "<custom_field>":{"set":[<value>]},
                        ...
                    }
                }
            }
        }
    }

.. http:example:: curl wget python-requests
   :request: ./publication/request.set-document-tags.txt
   :response: ./publication/response.set-document-tags.txt


Get Raw Content of a Publication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method allows users to get raw content of a document. It sends back the zen
content of the publication. If Fctx is used, content will be highlighted using
html tags in both title and text results : ``<hl class="focus-6">...</hl>``


**Request**
   ``GET`` https://radarly.linkfluence.com/1.1/projects/:pid/raw.json
**Headers**
   * *Authorization*: Bearer XXX
**Path Parameter**
   * pid: project id
**Query String Parameter**
   * uid: document id
   * platform: document source type, ie. ``blog``, ``dailymotion``,
     ``website``, ``forum``, ``twitter``, ``media``, ``instagram``,
     ``gplus``, ``facebook``, ``linkedin``, ``youtube``, ``comment``,
     ``vkontakte``, ``youku``, ``wechat``


.. http:example:: curl wget python-requests
   :request: ./publication/request.get-raw-publication.txt
   :response: ./publication/response.get-raw-publication.txt


Get Metrics Related to a Publication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method allows users to get metrics about one document. It sends back all
the metrics of the publication.

.. warning:: To use the raw-metrics route, you need to authorize an access to
    your Social Networks Credentials in the platforms settings
    (Settings->Social Accounts) or ask your account manager.


**Request**
   ``GET`` https://radarly.linkfluence.com/1.1/projects/:pid/raw-metrics.json
**Headers**
   * *Authorization*: Bearer XXX
**Path Parameter**
   * pid: project id
**Query String Parameter**
   * uid: document id
   * platform: document source type, ie. ``blog``, ``dailymotion``,
     ``website``, ``forum``, ``twitter``, ``media``, ``instagram``,
     ``gplus``, ``facebook``, ``linkedin``, ``youtube``, ``comment``,
     ``vkontakte``, ``youku``, ``wechat``
   * from (optional)
   * to (optional)


**Structure of the response**::

    {
        "metrics":{               # list of metrics
            <string> : <int>      # level by type of metrics when available by platforms eg. `likes`, `comments`, `twitter-api-rts`, `like_reactions`
        },
    }

.. http:example:: curl wget python-requests
   :request: ./publication/request.get-metrics-related-to-a-publication.txt
   :response: ./publication/response.get-metrics-related-to-a-publication.txt
