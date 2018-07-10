"""
Useful functions to perform efficient data mining's tasks on a dictionary
"""

import operator
import re

from .colorizer import blue, red
from .misc import extract_type


SEPARATOR_DPATH = re.compile(r'(.(?P<key>[\w]+)'
                             r'(\[(?P<index>[-\d]+)\])?'
                             r'(\((?P<filters>[ #&\(\)*+,.!/:;<=>?@\[\\\]^_`\{|\}~/,\w-]+)\))?)')
CORRECT_DPATH = re.compile(r'(^(\$|\$\$))({})*$'.format(SEPARATOR_DPATH.pattern))


def draw_structure(element, max_depth=2, indent=2, show_type=True, level=0):
    """
    Recursive function to draw the structure of a dictionary.

    Args:
        element (tuple): tuple where the first element is the name of the
            object to examine and the second one is the element itself
        max_depth (int, optional): deeper level to explore. Default
            to 1.
        indent (int, optional): indentation of each level drawn. Default
            to 2
        show_type (bool, optional): whether or not display the type of
            element
        level (int, optional): current level of exploration. Internal
            use.
    Returns:
        None:
    """
    indent_spaces = ("|" + " " * (indent - 1)) * level
    name, data = element
    data_type = extract_type(data)

    if name:
        line = '{}{}'.format(indent_spaces, name)
        if show_type:
            if data_type == 'None':
                data_type = red('({})'.format(data_type))
            elif data_type == 'list' and data:
                first_type = extract_type(data[0])
                data_type = blue('({}[{}])'.format(data_type, first_type))
            else:
                data_type = blue('({})'.format(data_type))
            line += ' {}'.format(data_type)
        print(line)

    if level == max_depth: return None
    is_radarly_object = 'radarly' in str(type(data))
    if isinstance(data, list) and data:
        draw_structure(element=(None, data[0]),
                       level=level,
                       max_depth=max_depth,
                       indent=indent,
                       show_type=show_type)
    elif isinstance(data, dict) or is_radarly_object:
        if is_radarly_object:
            data = dict((key, getattr(data, key)) for key in data.keys())
        for key in sorted(data.keys()):
            draw_structure(element=(key, data[key]),
                           level=level + 1,
                           max_depth=max_depth,
                           indent=indent,
                           show_type=show_type)

    return None


def not_contains(container, element):
    """Antonym of :func:`operator.contains`"""
    return not operator.contains(container, element)


def parse_filter(filters):
    """Parse a filter string, like ``id=323``.

    Args:
        filters (str): string to parse
    Returns:
        dict: dictionary with 3 keys
            *op*
              function used to compare two elements. The operator in the
              filter string is mapped to a function of the `operator` module
            *key*
              key of the object which should be examined (first argument
              of *op* function)
            *value*
              value used to
    """
    if filters is None: return None
    pattern = r' #&\(\)*+,.!/:;<=>?@\[\\\]^_`\{|\}~/,\w-'
    key_pattern = r'^(?P<key>[{}]*)'.format(pattern)
    operator_pattern = r'(?P<operator>=|!=|<|>|>=|<=| in | notin )'
    value_pattern = r'(?P<value>[{}]*)$'.format(pattern)
    filter_pattern = re.compile(key_pattern + operator_pattern + value_pattern)
    match = filter_pattern.match(filters)

    op_dict = {
        '=': operator.eq, '==': operator.eq, '!=': operator.ne,
        '>': operator.gt, '>=': operator.ge,
        '<': operator.lt, '<=': operator.le,
        ' in ': operator.contains, ' notin ': not_contains
    }
    op_func = op_dict[match.group('operator')]

    value = match.group('value')
    if value == 'True': value = True
    if value == 'False': value = False
    try:
        value = float(value)
    except ValueError:
        pass

    if op_func in [operator.contains, not_contains]:
        return dict(value=match.group('key'), key=value.lower(), op=op_func)
    return dict(key=match.group('key'), value=value, op=op_func)


def return_item(item, key, silently=False):
    """Depending of the type of item, return the value corresponding to `key`
    or the attribute `key` of the object item.

    Args:
        item (dict or object): Python object to explore
        key (str): key to search in the object
        silently (bool, optional): whether or not the function should
            raises an error if key is not found. Default to False
    Returns:
        object:
    """
    if isinstance(item, dict):
        return item.get(key, None) if silently else item[key]
    return getattr(item, key, None) if silently else getattr(item, key)


def dpath(source, path):
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
    def get(element, path, silently=False):
        """Core function of the dpath function.

        Ars:
            element (object): element to explore.
            path (list[dict]): path to follow to get the
                element. Each item must be a dictionary with three keys:
                `key` is the name of the object you want to explore (eg
                a key of a dictionary or an attribute of an object),
                `filters` is a dictionary specifying how to filter a list
                (can be None) and `index` is the index of an element in a
                list (can be None)
            silently (bool, optional): whether or not the function
                should raises an error if the key in not found. Default
                to False.
        Returns:
            object:
        """
        def get_item(item, key, index, filters):
            """Get a value matching a key in an object."""
            right_item = return_item(item, key, silently)
            if isinstance(right_item, list) and index and right_item:
                return right_item[int(index)]
            if isinstance(right_item, list) and filters and right_item:
                right_item = [
                    item for item in right_item
                    if filters['op'](return_item(item, filters['key'], silently),
                                     filters['value'])
                ]
                if len(right_item) == 1: return right_item[0]
                return right_item
            return right_item

        if path and element:
            if isinstance(element, list):
                return [
                    get(get_item(item, **path[0]), path[1:], silently) for item in element
                ]
            return get(get_item(element, **path[0]), path[1:], silently)
        return element

    if CORRECT_DPATH.match(path):
        silently = path.startswith('$$')
        path = [
            dict(
                key=item.group('key'),
                index=item.group('index'),
                filters=parse_filter(item.group('filters')),
            ) for item in SEPARATOR_DPATH.finditer(path)
        ]
        return get(source, path, silently=silently)
    path = dict(
        key=path,
        index=None,
        filters=None,
    )
    return get(source, [path])
