Project
~~~~~~~

Get Project information
^^^^^^^^^^^^^^^^^^^^^^^^

This method allows users to retrieve project information. It sends back
information about the project.


**Request**
   ``GET`` https://radarly.linkfluence.com/1.1/projects/:pid.json
**Headers**
   * *Authorization*: Bearer XXX


**Structure of the response**::

    {
        "id" :             <int>,               # project id
        "label" :          <string>,            # project label
        "created" :        <date>,              # project creation date
        "updated" :        <date>,              # project last update date
        "docsCount" :      <int>,               # docs count in the project
        "corpora" :        <array>,             # project corpus objects
        "focuses" :        <array>,             # project query objects
        "dashboards" :     <array>,             # project dashbaord objects
        "socialAccounts" : {                    # project social accounts objects
            <string> :     <array>              # by platform, eg. "facebook", "twitter", etc.
        },
        "benchmarkEntities": <array>,           # project benchmark entities objects
        "limits" :         {                    # project implemented limits
            "maxVol":           <int>,          # Max Volume of document in the project
            "maxTopics":        <int>,          # Max number of dashboards in the project
            "maxFocus":         <int>,          # Max number of Focus queries in the project
            "maxSearch":        <int>,          # Max number of Search queries in the project
            "maxSocialAccounts": <int>,         # Max number of Social Accounts in the project,
            "maxEntities":      <int>,          # Max number of Benchmark Entities in the project
            "maxSocialAccountByPlaform": <int>, # Max number of Social Accounts by Social platform
            "maxLiveStreams":   <int>,          # Max number of Stream in the liveStream page
            "maxCorpus":        <int>,          # Max number of Corpus in the project
            "maxSourceInCorpus": <int>,         # Max number of Source in each Corpus
            "maxTranslationBudget": <int>,      # Max budget for translation options
            "start" :           <date>,         # Project begining date
            "stop" :            <date>,         # Project end data
            "pack":             <string>        # Name of the Sales Pack
        },
        "tags" :          {                   # project tags objects
            "user":           <array>           # list of tags objects created to tag authors
            "custom"          <array>           # list of tags objects created by the user to tag posts
        },
        "platforms" :     <array>,            # project available platforms
    }


.. http:example:: curl wget python-requests
   :request: ./project/request.get-project-infos.txt
   :response: ./project/response.get-project-infos.txt
