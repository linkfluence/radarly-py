Installation
~~~~~~~~~~~~

.. _Github: https://github.com/linkfluence/radarly-py
.. _pypi: https://pypi.org/project/radarly-py/

The ``radarly-py`` package can be found in the official packages index pypi_
and on Github_, so there is two different ways to install it. The most updated
version in on Github but the package on Pypi will often be updated.

With ``pip``
++++++++++++

``radarly-py`` has been deployed on pypi_ so you can install it as any Python
packages with ``pip``.

.. code-block:: python

    pip install radarly-py

This command will install ``radarly-py`` in the current environment with all
its dependencies.


With Github_
++++++++++++

.. code-block:: bash

    git clone https://github.com/linkfluence/radarly-py
    cd radarly-py/
    python setup.py install

Instead of ``python setup.py install``, you can use ``pip install .``.


.. note:: ``pandas`` is not a dependency for ``radarly-py`` but we strongly
    advise you to install it in the same time because it will be very useful
    to explore some objects defined by the Python's client.
