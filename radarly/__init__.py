"""
`radarly-py` : a python's client for Radarly's API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Author: Linkfluence SAS
:Version: 1.0.0
:Licence: MIT

.. _official documentation: https://api.linkfluence.com

This package, developed by Linkfluence SAS is a Python's client in order to
ease interactions with the official REST API of Radarly product. ``radarly-py``
was designed in order to be compatible with standard Python's objects but also
with ``pandas`` and with the JSON format. You want to transform a pivot table
into a ``DataFrame``? Make it simply with ``pandas.DataFrame(my_pivot_table)``.
You want to serve your user's datas with a server: serialize your datas with
``my_current_user.json()``.
Please read the `official documentation`_ of the project to know all you can
do with this Python client and feel free to report any bug or suggestion you
have to our developer team.


Some informations about this package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This package was build by trying to respect the architecture of Radarly's
product. Most objects which exists in the product have been translated in the
client. It may have some differences but there are reported and not
significant.

.. warning:: Some objects like the dashboard can have minor importances in the
    client compared with the product.


About the objects
^^^^^^^^^^^^^^^^^
The ``radarly-py`` module uses mainly two kind of objects:

* object which inherits from ``SourceModel`` which only store informations.
  The objects ``Project``, ``User``, ``Tag`` or ``Dashboard`` are build on
  this model. These objects aim to give you access to all your informations
  stored in our databases. All objects of this types share some methods as
  ``draw_structure`` in order to ease the comprehension of Radarly's data
  models. Each object has also some specific methods in order to navigate
  in the API (for example, you can get some distribution statistics directly
  from a ``Project`` object using the ``get_analytics`` method). Check the
  documentation of each object to get some help on how to use it.
* object storing quantitative datas, which are based on ``list`` or ``dict``.
  These objects, as ``Analytics``, ``PivotTable`` or ``Distribution``, are
  build to be easily parsed with ``pandas``.

Most objects defined in ``radarly-py`` are documented. You can get more
informations on how to use it with the tutorials.
"""

from radarly.api import RadarlyApi


__title__ = 'radarly'
__version__ = '1.0.0'
__author__ = 'Linkfluence SAS'
__url__ = 'https://api.linkfluence.com'
__licence__ = 'MIT'
__copyright__ = 'Copyright 2018 Linkfluence SAS'
