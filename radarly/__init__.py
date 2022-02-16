"""
`radarly-py` : a python client for Radarly API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Author: Linkfluence
:Version: 1.0.12
:Licence: Apache-2.0

.. _official documentation: https://api.linkfluence.com
.. _quickstart tutorials: https://api.linkfluence.com/python/quickstart.html#use-cases

This package, developed by Linkfluence is a Python client in order to
ease interactions with the official REST API of Radarly products. ``radarly-py``
was designed in order to be compatible with standard Python objects but also
with :mod:`pandas` and with the JSON format. You want to transform a pivot table
into a :class:`pandas.DataFrame`? Make it simply with
``pandas.DataFrame(my_pivot_table)``. You want to serve your user's data with
a server: serialize your object with ``my_current_user.json()``.
Please read the `official documentation`_ of the project to know all you can
do with this Python client and feel free to report any bug or suggestion you
have to our developer team.


Some information about this package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This package was built by trying to respect the architecture of Radarly. Most
objects which exists in the product have been translated in the
client.


About the objects
^^^^^^^^^^^^^^^^^
The ``radarly-py`` module uses mainly two kind of objects:

* object which inherits from the ``SourceModel`` and stores information.
  The objects ``Project``, ``User``, ``Tag`` or ``Dashboard`` are built on
  this model. These objects aim to give you access to all your qualitative data
  stored in our databases. All objects of this types share some methods as
  ``draw_structure`` in order to ease the comprehension of Radarly's data
  models. Each object has also some specific methods in order to navigate
  in the API (for example, you can get some distribution statistics directly
  from a ``Project`` object using the ``get_analytics`` method). Check the
  documentation of each object to get some help on how to use it.
* object storing quantitative data, which are based on :class:`list` or ``dict``.
  These objects, like ``Analytics``, ``PivotTable`` or ``Distribution``, are
  build to be easily parsed with ``pandas``.

Most objects defined in ``radarly-py`` are documented. You can get additional
information on how to use it with the `quickstart tutorials`_.
"""

from radarly.api import RadarlyApi


__title__ = 'radarly'
__version__ = '1.0.12'
__author__ = 'Linkfluence'
__url__ = 'https://api.linkfluence.com'
__licence__ = 'Apache-2.0'
__copyright__ = 'Copyright 2018 Linkfluence'
