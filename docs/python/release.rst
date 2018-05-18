Releases
--------

.. role:: underline
    :class: underline


History
^^^^^^^

1.0.1
    :underline:`Release Date:` 2018/5/18

    This release corrects some bugs and add a large part of the documentation
    (especially use case tutorials).

    - Switch to Apache-2.0 license
    - Correct ``get_all_influencers`` method in ``radarly.project.Project``
    - Add proxies and timeout in ``authenticate`` and ``refresh`` methods of
      ``radarly.api.RadarlyApi``
    - Minor fixes to download publication
    - Correct parsing of ``radarly.pivottable.PivotTable`` object
    - Add ``geofiter`` method in ``radarly.parameters.DistributionParameter``
      and ``radarly.parameters.SearchPublicationParameter``
    - Correct making of url in ``radarly.api.RadarlyApi``
    - Correct ``refresh`` method in ``radarly.api.RadarlyApi``
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
