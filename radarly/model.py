"""
Model used in ``radarly-py``
"""

import copy
import json
from abc import ABC, abstractmethod

from pytz import timezone

from .api import RadarlyApi
from .utils.jsonparser import RadarlyEncoder
from .utils.path import dpath, draw_structure


class SourceModel:
    """Mixin to transform dictionary into an object where the keys of the
    dictionary are attributes of the instance"""
    _TRANSLATOR = dict(
        timezone=timezone
    )

    def __init__(self, data=None, translator=None):
        if data is None: data = dict()
        self.add_data(data, translator)

    def add_data(self, data, translator=None):
        """Add all (key, value) of data in the object

        Args:
            data (dict): data to transfer to the new object
            translator (dict, optional): translator to convert some value of the dict
        Returns:
            None:
        """
        translator = translator or dict()
        data = {
            key: translator.get(key, lambda x: x)(data[key])
            for key in data.keys()
        }
        self.__dict__.update(data)
        return None

    def __getitem__(self, path):
        """Quickly explore and find specific values in an object by following a
        path. This path must respect some format rules in order to be correctly
        understood by the function.

        * The path must begin with ``$``. If the path starts with ``$$``, the
        function will not raise an error if a key specified in the path is not
        found but will return None instead. If the ``path`` doesn't start with
        ``$``, the behaviour of the function is the same as the standard
        ``__getitem__`` function.
        * Each key of the path must be separated with a point ``.``
        * If you want to get only one element of a list, you can specify the index
        of the element, as in ``dashboards[3]``.
        * You can filter a list to only retrieve items matching a criteria. The
        criteria must be between parenthesis. The supported operator are: =, !=,
        <=, >=, >, <, in, notin

        **Example of valid paths**:

        * ``$.focuses[3].id``
        * ``$$.projects(id>50).limits.stop``
        * ``$.projects(DEMO in label).id``

        **Example of not valid paths**:

        * ``focuses[3].id`` (doesn't start with ``$``)

        Args:
            source (dict): object to explore
            path (str): path conformed to a JSON path
        Returns:
            object: object matching the dpath.
        """
        return dpath(self, path)

    def draw_structure(self, max_depth=5, show_type=True):
        """Draw the structure of an element

        Args:
            max_depth (int, optional): Default to 5.
            show_type (bool, optional): Default to True
        Returns:
            None:
        """
        draw_structure(element=(self.__class__.__name__, self),
                       level=0, max_depth=max_depth,
                       show_type=show_type, indent=2)
        return None

    def keys(self):
        """Returns a set of available attribute."""
        return {key for key in self.__dict__ if not key.startswith('_')}

    def json(self, **kwargs):
        """Serialize the object in order to have a dict object"""
        return json.dumps(self, cls=RadarlyEncoder, **kwargs)


class GeneratorModel(ABC):
    """Generator which yields all items matching some payload.

    Args:
        search_param (Parameter): parameter which should contains pagination
            parameters
        project_id (int, optional): identifier of the project
        api (RadarlyApi, optional): API used to perform request. If None,
            the default API will be used.
    Yields:
        object:
    """
    def __init__(self, search_param, project_id=None, api=None):
        self._api = api or RadarlyApi.get_default_api()
        self.project_id = project_id
        self.total = 0
        self.total_page = 0
        self.search_param = copy.deepcopy(search_param)
        self._items = None
        self.current_page = 1
        self._fetch_items()

    def __iter__(self):
        return self

    @abstractmethod
    def _fetch_items(self):
        """Get next range of items"""
        raise NotImplementedError(("In order to use this mixin, you must "
                                   "implement the _fetch_items method"))

    def __next__(self):
        try:
            returned_value = next(self._items)
        except StopIteration:
            self.current_page += 1
            if self.current_page > self.total_page:
                raise StopIteration
            self._fetch_items()
            returned_value = next(self._items)
        return returned_value
