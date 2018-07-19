Releases
--------

.. role:: underline
    :class: underline


History
^^^^^^^


1.0.6
    :underline:`Release Date:` 2018/7/19

    - The :class:`radarly.milestone.Milestone` was created in order to parse
      the values associated to ``milestones`` in a project.

1.0.5
    :underline:`Release Date:` 2018/6/28

    - The :class:`radarly.corpus.InfoCorpus` and :class:`radarly.corpus.Corpus`
      object was defined in :mod:`radarly.corpus`. Thanks to these objects,
      you can now explore the content of a corpus in Radarly. Check the
      documentation of these two objects and the quickstart tutorials for an
      in-depth learning.
    - The function :func:`radarly.publication.set_publication_tags` was
      created in order to give you the opportunity to update a publication
      without having the full object :class:`radarly.publication.Publication`.
    - The field ``Content`` displayed in an
      :class:`radarly.exceptions.RadarlyHTTPError` error was improved in order
      to display the parsed content of the HTML response.


1.0.4
    :underline:`Release Date:` 2018/6/28

    - Add :func:`radarly.publication.Publication.set_tags`
      a publication. Check the documentation and the quickstart example
      to get all informations about this feature.
    - Some fields in the response of a request are now not converted into
      snake case format. For example, the field ``radar.tag`` of a publication
      is ignored during the parsing of the response of a request.


1.0.3
    :underline:`Release Date:` 2018/6/26

    - Improve error management.


1.0.2
    :underline:`Release Date:` 2018/6/15

    With this release comes a better management of authentication errors and a
    small (internal) refactoring.

    - If the authentication fails, the client raises an error which depend on
      the error's type.
    - An instance of :class:`radarly.api.RadarlyApi` now stores a copy of the
      :class:`radarly.utils.router.Router` (in the ``router`` attribute) used
      for each request.
    - The default scopes for an instance of :class:`radarly.api.RadarlyApi` has
      been changed to ``listening`` and ``social-performance`` (the scope
      ``historical-data`` has beeen removed).
    - The ``version`` class attribute in :class:`radarly.api.RadarlyApi` is now
      an instance attribute.
    - The :class:`radarly.api.RadarlyApi.set_version` method has been
      deleted (this is a small break compatibility but this method was useless
      so the minor of the version has not been upgraded).
    - All parsed dates are now unaware :class:`datetime.datetime` object.


1.0.1
    :underline:`Release Date:` 2018/5/18

    This release corrects some bugs and add a large part of the documentation
    (especially use case tutorials). This version is the minimal version of the
    client to install in order to have a functionnal client.

    - Switch to Apache-2.0 license
    - Correct :func:`radarly.project.Project.get_all_influencers`
    - Add proxies and timeout in :func:`radarly.api.RadarlyApi.authenticate`
      and :func:`radarly.api.RadarlyApi.refresh` methods
    - Minor fixes to download publication
    - Correct parsing of data used to initialize a
      :class:`radarly.pivottable.PivotTable` object.
    - Add :func:`radarly.parameters.DistributionParameter.geofiter`
      and :func:`radarly.parameters.SearchPublicationParameter.geofiter`
    - Correct build of url in :class:`radarly.api.RadarlyApi`
    - Correct :func:`radarly.api.RadarlyApi.refresh`
    - Major updates of documentation


1.0.0
    :underline:`Release Date:` 2018/4/27

    *(Initial Release)* The client offers read-only methods to connect with
    Radarly's API (for example, there is no special methods for the moment to
    set a tag on a document or to add an influencer to a corpora).


Policy
^^^^^^

Major
    The new version will contain break changes, so you will have to adapt your
    script.

Minor
    Some refactoring, small changes or bug fixes are introduced in the new
    version. Normally, there is no break change with these releases.

Hotfix
    The new version will only contains bug fixes or some typos corrections.


We advise you to often check the minor or hotfix releases for a full
working client.
