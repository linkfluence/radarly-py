Searching in the API
~~~~~~~~~~~~~~~~~~~~~

The Radarly Search API allows queries against the documents of your project.

Standard Query Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^

All parameters are optional except where noted.


+-----------------------------+------------+-------------------------------------------------------------------------+
|       Parameter             | Type       | Description                                                             |
+=============================+============+=========================================================================+
|        query                |  string    | A UTF-8 search query string of maximum 4K characters maximum, including |
|                             |            | operators. eg: “linkfluence AND radarly”                                |
+------------+----------------+------------+-------------------------------------------------------------------------+
|        platforms            |  array     | Restricts to the given source types: `blog`, `dailymotion`, `website`,  |
|                             |            | `twitter`, `media`, `instagram`, `gplus`, `facebook`, `linkedin`,       |
|                             |            | `vkontakte`, `youku`, `wechat`, `comment`, `forum`, `youtube`.          |
+------------+----------------+------------+-------------------------------------------------------------------------+
|        language             |  array     | Restricts to the given languages, given by an                           |
|                             |            | `ISO 639-1 code <https://en.wikipedia.org/wiki/ISO_639-1>`_             |
+------------+----------------+------------+-------------------------------------------------------------------------+
|        gender               |  array     | Restricts to the given genders: M or F                                  |
+------------+----------------+------------+-------------------------------------------------------------------------+
|            | gt             |  date      | Restricts to the min birthdate date of the author                       |
| birthdate  +----------------+------------+-------------------------------------------------------------------------+
|            | lt             |  date      | Restricts to the max birthdate date of the author                       |
+------------+----------------+------------+-------------------------------------------------------------------------+
|        hasChildren          |  bool      | Restricts to author that declare to have children true or not false     |
+------------+----------------+------------+-------------------------------------------------------------------------+
|        inRelationship       |  bool      | Restricts to author that declare to be in a relationship true or not    |
|                             |            | false                                                                   |
+------------+----------------+------------+-------------------------------------------------------------------------+
|        verified             |  bool      | Restricts to author with certified accounts true or not verified false  |
+------------+----------------+------------+-------------------------------------------------------------------------+
|        tones                |  array     | Restricts to the given tones: positive, negative, neutral, mixed        |
+------------+----------------+------------+-------------------------------------------------------------------------+
|        media                |  array     | Restricts to the given media types:image or video                       |
+------------+----------------+------------+-------------------------------------------------------------------------+
|            | hastags        |    array   | Restrics to the given hashtags                                          |
+            +----------------+------------+-------------------------------------------------------------------------+
|            | mentions       |    array   | Restrics to the given @mentions                                         |
+  keywords  +----------------+------------+-------------------------------------------------------------------------+
|            | keywords       |    array   | Restrics to the given keywords (manual or trigger tags)                 |
+            +----------------+------------+-------------------------------------------------------------------------+
|            | namedEntities  |    array   | Restrics to the given named entities.                                   |
+------------+----------------+------------+-------------------------------------------------------------------------+
|            | charts         |  array     | Restrics to the given emoji (char - example \*)                         |
| emoji      +----------------+------------+-------------------------------------------------------------------------+
|            | annotations    |  array     | Restrics to the given emoji (annotations - example arrow)               |
+------------+----------------+------------+-------------------------------------------------------------------------+
|            | gt             |  int       | Restricts to the min number of followers of a twitter/instagram         |
|            |                |            | /sinaweibo source.                                                      |
| followers  +----------------+------------+-------------------------------------------------------------------------+
|            | lt             |  int       | Restricts to the max number of followers of a twitter/instagram         |
|            |                |            | /sinaweibo source.                                                      |
+------------+----------------+------------+-------------------------------------------------------------------------+
|            | favorite       | bool       | Enables the retrieving of favorites or non-favorites. default: false    |
+            +----------------+------------+-------------------------------------------------------------------------+
| flag       | rt             | bool       | Enables the retrieving of trashed publications - default: false         |
+            +----------------+------------+-------------------------------------------------------------------------+
|            | trash          | bool       | EnableS the retrieving of retweets - default false                      |
+------------+----------------+------------+-------------------------------------------------------------------------+
|        from                 |  datetime  | Start datetime of the time period (publication date of the document)    |
+------------+----------------+------------+-------------------------------------------------------------------------+
|        to                   |  datetime  | End datetime of the time period (publication date of the document)      |
+------------+----------------+------------+-------------------------------------------------------------------------+
|            | createdBefore  |  datetime  | Start datetime of the time period (indexed date of the document)        |
| date       +----------------+------------+-------------------------------------------------------------------------+
|            | createdAfter   |  datetime  | End datetime of the time period (indexed date of the document)          |
+------------+----------------+------------+-------------------------------------------------------------------------+
|            | type           |  array     | Restricts to the givent type of geographic localization: country or town|
| geo        +----------------+------------+-------------------------------------------------------------------------+
|            | list           |  array     | List of items following geo.type - fr, gb; Restricts to the given       |
|            |                |            | languages, given by an ISO 3166-1 alpha-2)                              |
+------------+----------------+------------+-------------------------------------------------------------------------+
|        focuses              |  array     | List of the Radarly registred query ids you want to search into         |
+------------+----------------+------------+-------------------------------------------------------------------------+
|        corpora              |  array     | List of the Radarly registred corpora ids you want to search into       |
+------------+----------------+------------+-------------------------------------------------------------------------+
|                             |  array     | List of the Radarly categories (listed at the end of this page) you     |
|           categories        |            | want to restrict your search. For exemple:                              |
|                             |            | categories:["business.luxury"]                                          |
+------------+----------------+------------+-------------------------------------------------------------------------+
|            | userTags       |  array     | List of Radarly registred influencers group tags you want to restrict to|
| tags       +----------------+------------+-------------------------------------------------------------------------+
|            | customFields   |  array     | List of custom Fields values under format you want to restrict to.      |
|            |                |            | Example::                                                               |
|            |                |            |                                                                         |
|            |                |            |    customFields: {                                                      |
|            |                |            |       "Main topic": ["Sponsoring"],                                     |
|            |                |            |       "Products": ["shoes"]                                             |
|            |                |            |    }                                                                    |
+------------+----------------+------------+-------------------------------------------------------------------------+



Query Syntax
^^^^^^^^^^^^

The query parameter query can have operators that modify its behavior, the available operators are explained below. Search, Focus, and Trigger queries as Filters search have the same syntax.


Case & special characters
*************************

By default, text is indexed and queried.

* in lower-case: Query strings are case insensitive: searching ``Bonjour`` and ``bonjour`` will retrieve the same results.
* with all the diacritics removed (``é``, ``ç``, ...).
* symbols transformed into space character: searching ``jean-jacques`` and ``jean jacques`` will retrieve the same results. Here are a non exhaustive list of characters that are not indexed: comma ``,``, colon ``:``, dot ``.``, semicolon ``;``, hyphen ``-``, slash ``/``, question mark ``?``, exclamation mark ``!``, percent sign ``%``, tilde ``~``, parentheses ``(`` ``)``, brackets ``[`` ``]``, braces ``{`` ``}``, plus sign, equal sign ``=``, ampersand ``&``, dollar sign ``$``, euro sign ``€``, apostrophe ``‘``.
* underscore (``_``) is indexed like a classic character.

Radarly searches for exact expressions. This means that if you choose the keyword ``yamaha``, ``yamahamotors`` will not match your query. When writing queries, use lower case letters without accents: write ``barack obama” OR elephant`` instead of ``Barack Obama OR éléphant`` (but using accents and special characters in a query do not have an impact in Radarly.)

Boolean
*******

Must / Must not
***************

These operators are prefered to the classical AND and NOT operators because they are less complex (from a computer point of view) and thus faster! From ElasticSearch, the preferred operators are + (this term ‘'’must’’’ be present) and - (this term ‘'’must not’’’ be present). All other terms are optional.

Operators
*********

Single word
***********
Single string without operator will retrieve document with the exact same string. ``activia`` will retrieved documents with the exact same string “activia”


Expression
**********
The double-quote character allows the exact match query. Searching ``“john smith”`` will retrieve documents where the exact compound “john smith” is present. The wildcard does not work with expressions between quotes (eg. ``“activia nature*”``).

``AND`` operator
********************
``car AND red`` will retrieved documents in which car and red are present without any proximity constraints.

``(car* AND red) OR (bus* AND blue)`` will retrieved documents in which car(s) and red are present or/and blue and bus(es) are present.

``((car* OR bus*) AND (red OR blue))`` will retrieved : red car, red cars, blue car, blue cars, blue bus, blue buses, red bus, red buses …

``OR`` operator
*******************
``car OR bicycle``: The operator OR is not exclusive. This means that you will retrieve documents in which car OR bicycle are present but also when car and bicycle are present.

``NOT`` operator
********************
``NOT nike`` will retrieve all the publications that do not contain “nike”.

``adidas NOT nike`` will retrieve all the publications that contain “adidas” and do not contain “nike”.

Wildcard ``*`` operator
***************************
You can use the wildcard character ``*`` to search for suffix part of words.

``operation*`` <ill retrieve documents containing “operation”, “operations”, “operational”, etc. Mono Wildcard operator ``“?”`` can be replaced by another letter maga?ine OR operation? to search for : maga?ine => Will find mentions magazine or magasine

Tilde ``~`` operator
************************

``"activia danone"~5`` will retrieve documents where both “activia” and “danone” words are present within a range of 5 words (cf. `PhraseQuery and edit distance slightly confusing <http://www.gossamer-threads.com/lists/lucene/java-user/33550>`_).

Tilde works with the operator NEAR


``NEAR/`` operator
**********************
``(activia AND yogurt) NEAR/8 (danone)`` can match:

* The Activia yogurt is one of the best products of Danone.
* The Activia yogurt is a product of Danone.
* Danone is a brand of Activia yogurt.

Proximity operator ``«``
****************************
A proximity operator where order is important and a maximum distance. ``activia <<4 yogurt`` matches:

* Activia is a brand of yogurt
* Activia is a yogurt brand
* Doesn’t match: Danone’s yogurt brand is Activia

``yogurt <<4 activia`` matches "My favorite yogurt is Activia".

Quorum operator ``/``
*************************
``"yogurt danone activia"/2``: it will retrieve publications that contain 2 words out of the three (yogurt, danone and activia).

Keywords operators
******************

title
   ``danone AND title:activia``

text
   ``text:activia AND text:danone``
   ``text:(activia AND danone)``

raw
   Copy of the text field, case insensitive, but with some caracters kept:

   * currency symbols (cf. `List of currency symbols <http://www.unicode.org/charts/PDF/U20A0.pdf>`_ for a nearly exhaustive list of them). Currency symbols are parsed as individual token so: 5€ becomes <5> <€>. “,-“ are ignored so “5,-€” becomes <5> <€> as well. The phrase query “5€” matches every <5> token followed by token <€>.
   * hashtags (#word) and at-signs (@name) as defined by Twitter (cf. `Using hashtags on Twitter <https://support.twitter.com/articles/49309-using-hashtags-on-twitter>`_ and `Why can’t I register certain usernames? <https://support.twitter.com/articles/101299-why-can-t-i-register-certain-usernames#error>`_);
   * the + symbol but only at the end of a word:
   * me+you => me you
   * canal+ => canal+
   * the &, - and / symbols but only between two words without space:
   * directory/ => directory
   * h&m => h&m

   Examples:

   ``raw:"h&m" AND raw:"t-shirt" AND red``
   ``raw:("h&m" AND "t-shirt") AND red``
   will retrieve publications that contain the “h&m” or “H&M” words associated with “t-shirt” or “T-shirt” and “red” but not those that contain “h m” or “t shirt”.

rawer
   The same field as raw: but case sensitive!

   ``rawer:Apple`` will retrieve publications that contain the “Apple” word but not those that contain “apple”.

   ``rawer:H&M`` will retrieve publications that contain the “H&M” word but not those that contain “h&m” or “h m”.

Hashtags #
   ``hashtag:ilavaitpasprissonactimel`` ou ``#ilavaitpasprissonactimel``

   .. warning:: ``#`` doesn’t work with NEAR

   On Twitter, if we simply look for a hashtag, always write the hashtag with the #. But if we want to search for a hashtag as well as a word, enter the the hashtag with and without the #. Not only the bare word. Some retweets exceed 140 characters and are therefore cut off. When you query for a hashtag that has been cut, we miss these posts. The hashtags being cut off, you lose the ability to query on these hashtags. One workaround for this truncated hashtag problem, is to retrieve information in the general meta-information so that we can recover these publications.

Screen names
   ``<platform>.mentions.screen-name:linkfluence OR @linkfluence OR <platform>.mentions.id:15842878``

   .. warning:: Attention

      * Case sensitive
      * Doesn’t match “linkfluence”


Specific Author
^^^^^^^^^^^^^^^
``"user.<platform>.<platform_user_id>"`` to search on a specific author on a specific platform. The user_id is the one attributed by the platform.

Stories
^^^^^^^
To search on a specific clusters publications, use the search parameter “stories” and the list of stories_ids:
``"stories:["<story_id>"]"``

Categories
^^^^^^^^^^
We developed an algorithm extracting and categorizing posts by topics. Topics of Level 1 and 2 are a predefined list of top level categories and subcategories. The available categories are:

business
   *luxury*, *market*, *transport*, *your-money*

ecology
   *biodiversity*, *climatic*, *energy*, *farming*, *natural-disaster*, *pollution-recycling*

entertainment
   *arts*, *books*, *comics*, *history*, *movies*, *music*, *theater-dance*, *tv-radio*, *video-games*

lifestyle
   *auto-moto*, *beauty*, *family*, *fashion*, *food*, *home-garden*, *people*, *professional-life*, *seduction*, *travel*, *wedding*, *wellness*

media
   *buzz*, *communication*, *medias*

politics
   *africa*, *americas*, *asia-pacific*, *europe*, *france*, *middle-east*, *usa*

society
   *education*, *employment*, *health*, *justice*, *security*, *social*

sports
   *american-football*, *athletics*, *badminton*, *basketball*, *biathlon*, *bobsleigh*, *bodyboard*, *boxing*, *crosscountry-skating*, *curling*, *cycling*, *equestrian*, *figure-skating*, *football*, *formula1*, *golf*, *handball*, *ice-hockey*, *kitesurf*, *motorsport*, *rugby*, *sailing*, *skateboard*, *ski-jumping*, *snowboard*, *squash*, *surf*, *swimming*, *table-tennis*, *taekwondo*, *tennis*, *volleyball*, *windsurf*, *winter-sport*, *wrestling*

technology
   *computer*, *mobile-device*, *science*, *startup-digital*