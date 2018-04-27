"""
Hooks used to parse JSON data contained in the response of a request.
"""

import re
from datetime import datetime
import json

import pytz
from dateutil.parser import parse

from .misc import to_snake_case


def radarly_decoder(obj):
    """Hook which can be used in the `dumps` function of `json` module."""
    def decode_value(value, key=None):
        """Try to convert a string into a specific Python's object"""
        pattern_date = re.compile(
            r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z'
        )

        if isinstance(value, str) and pattern_date.match(value):
            return parse(value)
        elif key == 'timezone' and value in pytz.all_timezones_set:
            return pytz.timezone(value)
        return value
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
