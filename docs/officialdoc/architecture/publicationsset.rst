Set of Publications
~~~~~~~~~~~~~~~~~~~

Get Keywords, Hashtags, Mentions, etc. for Publications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method allows users to retrieve all the most relevant keywords
about a query or a set of queries:

* keywords (trigger keywords + manual keywords)
* hashtags
* mentions
* namedEntities (aggregation of people, organizations, locations, miscellaneous)
* affects
* emojis (under the Charts 💖 or Annotations “heart” format)

It sends back a global JSON document with all the distributions broken down by keyword types.

**Request**
   ``POST`` https://radarly.linkfluence.com/1.0/projects/:pid/insights/cloud.json
**Headers**
   * *Authorization*: Bearer XXX
**Path Parameter**
   * pid: project id
**Payload Parameter**
    Habitual Search Parameter + Following Parameter

    ========= ======== ===============================================================
    Parameter Type     Description
    ========= ======== ===============================================================
    tz        string    Timezone, formated according to the tz database: Europe/Paris
    metrics   array     List of the metrics returned in the statistics - Allowed
                        metrics - ``doc``, ``impression``, ``reach``, ``engagements``,
                        ``repost``.
    fields    array     List of the type of results returned in the statistics -
                        Allowed values - ``keywords``, ``hastags``, ``mentions``,
                        ``namedEntities``, ``affects``, ``emojis`` (By default:
                        ``keywords``, ``mentions``, ``namedEntities``, ``hastags``)
    ========= ======== ===============================================================

.. http:example:: curl wget python-requests
   :request: ./publicationsset/request.get-publications-keywords.txt
   :response: ./publicationsset/response.get-publications-keywords.txt


Get Localizations
^^^^^^^^^^^^^^^^^
This method allows users to retrieve the distribution of publications by
geographical zones. Sends back a global JSON document with all the
distributions and information about the locations (name, lang, lat,
lng, population, etc…)

**Request**
   ``POST`` https://radarly.linkfluence.com/1.0/projects/:pid/insights/geo/:type.json
**Headers**
   * *Authorization*: Bearer XXX
**Path Parameter**
   * pid (*string*): project id
   * type (*string*): type of geography
**Query String**
   * locale (*string*): locale of the user to display the labels of the
     geographical zones, ie. ``en_GB``, ``fr_FR``
**Payload Parameter**
    Standard Search Parameter + Following Parameter

    ========= ======== ===============================================================
    Parameter Type     Description
    ========= ======== ===============================================================
    tz        string    Timezone, formated according to the tz database: Europe/Paris
    metrics   array     List of the metrics returned in the statistics - Allowed
                        metrics - ``doc``, ``impression``, ``reach``, ``engagements``,
                        ``repost``.
    ========= ======== ===============================================================

.. http:example:: curl wget python-requests
   :request: ./publicationsset/request.get-localizations.txt
   :response: ./publicationsset/response.get-localizations.txt


Get Distributions
^^^^^^^^^^^^^^^^^

This method allows users to retrieve publications volume/impression/reach
distribution. Sends back a global JSON document with all the distributions.

**Request**
   ``POST`` https://radarly.linkfluence.com/1.0/projects/:pid/inbox/distribution.json
**Headers**
   * *Authorization*: Bearer XXX
**Path Parameter**
   * pid (*string*): project id
**Payload Parameter**
    Standard Search Parameter + Following Parameter

    ========= ======== ===============================================================
    Parameter Type     Description
    ========= ======== ===============================================================
    metrics   array     List of the metrics returned in the statistics - Allowed
                        metrics - ``doc``, ``impression``, ``reach``, ``engagements``,
                        ``repost``.
    ========= ======== ===============================================================


.. http:example:: curl wget python-requests
   :request: ./publicationsset/request.get-publications-distribution.txt
   :response: ./publicationsset/response.get-publications-distribution.txt


Get Publications Statistics
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method allows users to retrieve all the statistics about a query or a set of queries:

* Countries distribution
* Queries distribution
* Keywords distribution
* Languages distribution
* Platforms distribution
* Tonality distribution
* Genders distribution
* Topic categories distribution
* Occupations distribution
* Demography distribution
* Logos distribution
* Custom fields distribution (any custom field you created inside your project)


**Request**
   ``POST`` https://radarly.linkfluence.com/1.0/projects/:pid/inbox/insights.json
**Headers**
   * *Authorization*: Bearer XXX
**Path Parameter**
   * pid: project id
**Payload Parameter**
    Habitual Search Parameter + Following Parameter

    ========= ======== ===============================================================
    Parameter Type     Description
    ========= ======== ===============================================================
    fctx      array     Registred queries in Radarly (id) used to compute the
                        distribution of volume.
    metrics   array     List of the metrics returned in the statistics - Allowed
                        metrics - ``doc``, ``impression``, ``reach``, ``engagements``,
                        ``repost``.
    fields    array     List of the type of results returned in the statistics -
                        Allowed values ``keywords``, ``platforms``, ``focuses``,
                        ``tones``, ``countries``, ``languages``, ``occupations``,
                        ``demography``, ``genders``, ``categories``, ``logos``,
                        ``<any_custom_field_name>``
    ========= ======== ===============================================================


.. http:example:: curl wget python-requests
   :request: ./publicationsset/request.get-publications-statistics.txt
   :response: ./publicationsset/response.get-publications-statistics.txt


Get Publications Clusters
^^^^^^^^^^^^^^^^^^^^^^^^^

This method allows users to retrieve all the clusters of publications


**Request**
   ``POST`` https://radarly.linkfluence.com/1.0/projects/:pid/inbox/stories.json
**Headers**
   * *Authorization*: Bearer XXX
**Path Parameter**
   * pid: project id
**Payload Parameter**
    Habitual Search Parameter + Following Parameter

    ========= ======== ===============================================================
    Parameter Type     Description
    ========= ======== ===============================================================
    metrics   array     List of the metrics returned in the statistics - Allowed
                        metrics - ``doc``, ``impression``, ``reach``, ``engagements``,
                        ``repost``.
    sortBy    array     Sorting parameter - ``volumetry`` or ``radar.impression`` or
                        ``radar.reach``
    sortOrder array     Sorting order - ``desc`` or ``asc``
    start     int      Starting index (used for pagination) Defaults to 0
    limit     int      Max number of results. Defaults to 25
    ========= ======== ===============================================================


.. http:example:: curl wget python-requests
   :request: ./publicationsset/request.get-publications-clusters.txt
   :response: ./publicationsset/response.get-publications-clusters.txt


Get Publications Topics
^^^^^^^^^^^^^^^^^^^^^^^

**Request**
   ``POST`` https://radarly.linkfluence.com/1.0/projects/:pid/topicwheel.json
**Headers**
   * *Authorization*: Bearer XXX
**Path Parameter**
   * pid (*string*): project id
**Query String**
   * locale (*string*): locale of the user to display the labels of the
     geographical zones, ie. ``en_GB``, ``fr_FR``
**Payload Parameter**
    Standard Search Parameter + Following Parameter

    ========= ======== ===============================================================
    Parameter Type     Description
    ========= ======== ===============================================================
    tz        string    Timezone, formated according to the tz database:
                        ``Europe/Paris``
    metrics   array     List of the metrics returned in the statistics - Allowed
                        metrics - ``doc``, ``impression``, ``reach``, ``engagements``,
                        ``repost``.
    ========= ======== ===============================================================

This method allows users to retrieve all the values to recreate Radarly’s
topic wheel. Sends back a global JSON document with all the distributions broken
down by keyword types.

.. http:example:: curl wget python-requests
   :request: ./publicationsset/request.get-publications-topics.txt
   :response: ./publicationsset/response.get-publications-topics.txt
