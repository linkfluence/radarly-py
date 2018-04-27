Social Performance
~~~~~~~~~~~~~~~~~~


Get Social Performance
^^^^^^^^^^^^^^^^^^^^^^
This method allows users to get social performance data (twitter, facebook, instagram and youtube).

**Request**
   ``GET`` https://radarly.linkfluence.com/1.0/projects/:pid/performance.json
**Headers**
   * *Authorization*: Bearer XXX
**Path Parameter**
   * pid (*string*): project id
**Query String**
   * platform (*string*): account source type: ie. ``twitter``, ``facebook``, ``instagram``, ``youtube`` or ``linkedin``
   * from (datetime, optional): start datetime of the time period
   * to (datetime, optional): end datetime of the time period
   * tz (string, optional): timezone, formated according to the tz database: ``Europe/Paris``

**Structure of the response**::

    {
    "Account_UID"
    └ "Stats"
        └ {"date":<date>,
        "Scores":{<all metrics names per platforms>:<values>}


.. http:example:: curl wget python-requests
   :request: ./socialperformance/request.get-social-performance.txt
   :response: ./socialperformance/response.get-social-performance.txt


Get Benchmark Statistics
^^^^^^^^^^^^^^^^^^^^^^^^

**Request**
   ``GET`` https://radarly.linkfluence.com/1.0/projects/:pid/benchmark.json
**Headers**
   * *Authorization*: Bearer XXX
**Path Parameter**
   * pid (*string*): project id
**Query String**
   * entities (*list*): entities list ids
   * from (datetime): start datetime of the time period
   * to (datetime): end datetime of the time period
   * tz (string): timezone, formated according to the tz database: ``Europe/Paris``

**Structure of the response**::

    {
        "facebook" : <array>,
        "instagram": <array>,
        "twitter": <array>,
        "youtube": <array>
    }


This method allows users to get benchmark data. Sends back all the data and metadata of the benchmark entities.

.. http:example:: curl wget python-requests
   :request: ./socialperformance/request.get-benchmark-statistics.txt
   :response: ./socialperformance/response.get-benchmark-statistics.txt
