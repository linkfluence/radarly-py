==========
radarly-py
==========

.. image:: https://img.shields.io/pypi/v/radarly-py.svg
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/radarly-py/

.. image:: https://img.shields.io/pypi/pyversions/radarly-py.svg
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/radarly-py/

.. image:: https://img.shields.io/pypi/l/radarly-py.svg
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/radarly-py/



:Author: Linkfluence
:Version: 1.0.9



.. _documentation: https://api.linkfluence.com/

This package is a Python client in order to use Radarly API. Thanks to
this client, you can fetch most of the endpoints described in the
`documentation`_.


Installation
^^^^^^^^^^^^
You can use ``pip`` to install this package. The commmand
``pip install radarly-py`` will install the package and all its dependencies.

.. note:: ``pandas`` is not a dependency of ``radarly-py`` but it is strongly
    advise to use to explore all objects storing quantitative data.


Quickstart
^^^^^^^^^^
First thing first, you must initialize an API.

>>> from radarly import RadarlyApi
>>> credentials = dict(client_id="XXXXX", client_secret="XXXXX")
>>> RadarlyApi.init(**credentials)
<RadarlyAPI.client_id=XXXXXXX>

Then, you can explore Radarly API with the different objects defined by
the client.

For example, you can explore all information about you (your projects,
your settings...).

>>> from radarly.user import User
>>> me = User.find(uid='me')
>>> me
<User.id=1.email='user.email@company.com'>
>>> me.draw_structure(max_depth=1)
User (User)
 | account_id (int)
 | apps (list[str])
 | can_create_project (bool)
 | connected (int)
 | connection_count (int)
 | created (datetime)
 | current_project_id (int)
 | email (str)
 | engagement (dict)
 | id (int)
 | is_disabled (bool)
 | is_internal (bool)
 | is_manager (bool)
 | is_pending (bool)
 | is_root (bool)
 | level (str)
 | locale (str)
 | name (str)
 | picture_id (None)
 | projects (list[InfoProject])
 | theme (str)
 | timezone (Europe/Paris)
 | updated (datetime)


Then, you can explore a specific project.

>>> from radarly.project import Project
>>> my_project = Project.find(pid=2)
>>> my_project
<Project.pid=2.label=IGIT>
>>> my_project.draw_structure(max_depth=1)
Project (Project)
 | account_id (int)
 | alcmeon_company (str)
 | benchmark_entities (list[dict])
 | brand_logos (list)
 | client_reference (str)
 | corpora (list[dict])
 | created (datetime)
 | credentials (dict)
 | dashboards (list[Dashboard])
 | docs_count (int)
 | docs_version (int)
 | flags (dict)
 | focuses (list[Focus])
 | id (int)
 | industries (list[dict])
 | label (str)
 | limits (dict)
 | milestones (list[dict])
 | mm3_id (None)
 | out_of_reach_count (int)
 | picture_id (int)
 | platforms (list[str])
 | project_manager_id (int)
 | renew (datetime)
 | research_manager_id (int)
 | sinaweibo_options (dict)
 | social_accounts (list[SocialAccount])
 | social_wall_text (str)
 | start (datetime)
 | stop (datetime)
 | tags (list[Tag])
 | total_indexed_docs_count (int)
 | updated (datetime)
>>> my_project['$.focuses.id'][:5]  # Top five focuses'id in the project
[154262, 154263, 154374, 5, 140519]


You can now get some publications stored in this project. For example, we will
retrieve five publications of the project, published in 2017 and matching the
query with the id 137622 (see ``project['focuses']`` to explore the queries
of your project).

>>> from radarly.parameters import SearchPublicationParameter()
>>> from datetime import datetime
>>> start, end = datetime(2017, 1, 1), datetime(2017, 31, 12)
>>> parameter = SearchPublicationParameter() \
    .publication_date(start, end) \
    .pagination(start=0, limit=5) \
    .focuses(include=[137622])
>>> publications = project.get_publications(parameter)
>>> publications
[<Publication.uid='r3_prod_2-10...6268444865350'>,
 <Publication.uid='r3_prod_2-10...6268441960350'>,
 <Publication.uid='r3_prod_2-989433433368748032'>,
 <Publication.uid='r3_prod_2-10...6268434280350'>,
 <Publication.uid='r3_prod_2-10...6268433470350'>]


This client gives you many possibilities to explore and navigate in
our API. Plese read the official `documentation`_ of the API and the
client to check all that is possible.
