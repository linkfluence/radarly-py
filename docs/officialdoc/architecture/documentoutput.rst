.. _documentouput:

Precision on Document Output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Regarding the type of the document, the list of available fields in a document output can differs:
    * Some Fields are specific to certain platforms:  ``"retweet"`` will only by available in Twitter Content
    * Some Fields are more or less detailed according to the right of the user (if you owned the content or not)
    * Some platforms are applying restriction on the distribution of content through APIs, you will need to use an alternate solution to access full content.

The search route will always returns all the available fields.

Restriction on Document Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some platforms are restricting the way content can be distributed through our API.
The reason a field may not be available to a document are the following:
	* The platform does not allow us in its terms of use to return all the content through our own APIs. For instance, Twitter is restricting the content to be distributed through APIs to only Tweet IDs, Direct Message IDs, and/or User IDs.
	* You are not granted to access this information. Some platforms restrict access to meta-data to the owner or to the recipient of the post.
	
Precision on restricted Twitter Content
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Twitter is restricting the content to be distributed through APIs to only Tweet IDs, Direct Message IDs, and/or User IDs. 
As a consequence:
	* fields like ``"name"``, ``"screenname"``, ``"gender"`` will not be displayed as a child to a ``"user"`` or a ``"mentions"``.
	* fields like ``"text"``, ``"url"`` or ``"media"`` will not be attached to a tweet

All the different fields and meta-data enrichments processed by Radarly will be delivered.
It does not affect the way Radarly is displaying the content of a Tweet in the front application, only the API output.

How to retrieve the link to a Tweet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    It is possible to create a *link to a tweet* by reconstructing the URL using the following patterns ``"https://twitter.com/<author_id>/status/<tweet_id>"``

How to display a Tweet on a website using the Tweet id
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is possible to display a tweet using Twitter tools:
	#. the Javascript API and the id of a tweet: `Javascript API <https://developer.twitter.com/en/docs/twitter-for-websites/javascript-api/overview>`_.
	#. the Oembed API and the url of a tweet: `GET statuses/oembed <https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-oembed>`_.

How to access the content of a Tweet or an Author using a list of Ids
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is possible to *access the content of a tweet or an author* by using the Twitter API.
	#. First, you need to register and create an app on the `Twitter Developer Website <https://developer.twitter.com/en/docs.html#/>`_.
	#. Using your app and credentials, you will be able to access:
		* Tweet Content by providing up to 100 tweet ids per calls using: `GET statuses/lookup <https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-users-lookup/>`_. (A user object is included as Author of a Tweet object)
		* User Content by providing up to 100 user ids per calls using: `GET users/lookup <https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-users-lookup/>`_. 
