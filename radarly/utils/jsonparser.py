"""
Hooks used to parse JSON data contained in the response of a request.
"""

import re
from datetime import datetime
import json

import pytz
from dateutil.parser import parse

from .misc import to_snake_case


_BLACKLIST_PATH = [
    ['hits', 'radar', 'tag'],
    ['radar', 'tag'],
    ['dots', 'stats'],
]


def decode_value(value, key=None):
    """Try to convert a string into a specific Python object"""
    pattern_date = re.compile(
        r'^ *\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z *$'
    )

    if isinstance(value, str) and pattern_date.match(value):
        return parse(value.strip(), ignoretz=True)
    elif key == 'timezone' and value in pytz.all_timezones_set:
        return pytz.timezone(value)

    return value


def radarly_decoder(obj):
    """Hook which can be used in the `dumps` function of `json` module."""
    return dict(
        (to_snake_case(key), decode_value(obj[key], key)) for key in obj
    )


class RadarlyEncoder(json.JSONEncoder):
    """Encoder to serialize an object which inherits from SourceModel"""
    def default(self, obj):
        if 'radarly' in str(type(obj)):
            return dict(
                (key, dict(obj)[key]) for key in obj.keys()
                if not key.startswith('_') and not callable(dict(obj)[key])
            )
        if 'pytz.' in str(type(obj)):
            return obj.zone
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        return json.JSONEncoder.default(self, obj)


def snake_dict(data, blacklist=None, path=[]):
    """Convert all the keys of a dictionary into snake case format. It will
    also convert some values into Python object (like all the dates or timezone
    field).
    Map automatically if the element is a list. Some path can be blacklisted
    and so they will not be converted in to snake_case format.

    Args:
        data (object): dictionary or list to convert
        blacklist (list[list[str]]): path to ignored during the parsing.
            Example: ``[['radar', 'tag', 'custom']]``
        path (list[str]): internal use.
    Returns:
        object: the same object with all keys converted into snake cas format
            and some values converted into Python object.
    """
    if isinstance(data, list):
        return [snake_dict(item,
                           blacklist=blacklist,
                           path=path) for item in data]

    if isinstance(data, dict) and path not in blacklist:
        return {
            to_snake_case(key): snake_dict(data[key],
                                           path=path + [key],
                                           blacklist=blacklist)
            for key in data
        }

    return decode_value(data, path[-1])
