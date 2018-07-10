"""
Miscellaneous functions and classes
"""

import json
import re
import textwrap
from collections import UserList, namedtuple
from datetime import datetime
from functools import reduce
from os.path import dirname, join, pardir
from urllib.parse import urlparse

from dateutil.relativedelta import relativedelta
from dateutil.rrule import MONTHLY, rrule


def load_data(filepath):
    """Load static file located in the package directory"""
    filepath = join(dirname(__file__), pardir, filepath)
    with open(filepath, mode='r') as data_file:
        data = json.load(data_file)
    return data


def dict_to_namedtuple(name, data):
    """Converts a dictionary into a namedtuple"""
    return namedtuple(name, data.keys())(**data)


flat = lambda x: reduce(lambda a, b: a+b, x, [])


class Quarter(UserList):
    """List object storing start date and end date of a quarter"""
    def __init__(self, n_quarter, year):
        super().__init__()
        self.n_quarter = n_quarter
        self.year = year
        start = datetime(year, 1, 1)
        start_quarter = list(
            rrule(MONTHLY, interval=3, dtstart=start, count=4)
        )[n_quarter - 1]
        end_quarter = start_quarter + relativedelta(months=3, days=-1)
        self.data.extend([start_quarter, end_quarter])

    def __contains__(self, value):
        return value >= self[0] and value <= self[1]

    @classmethod
    def of_year(cls, year):
        """Generates all Quarter object of a specific year"""
        start = datetime(year, 1, 1)
        start_quarter = list(
            rrule(MONTHLY, interval=3, dtstart=start, count=4)
        )
        end_quarter = [
            date + relativedelta(months=3, days=-1) for date in start_quarter
        ]
        return [cls(*item) for item in list(zip(start_quarter, end_quarter))]

    def __repr__(self):
        return '<Quarter.nth={}.year={}>'.format(
            1 + self.data[0].month // 3,
            self.data[0].year
        )


def parse_date(date_string):
    """Parse a date string with the format '%Y-%m-%dT%H:%M:%S.%fZ'.

    Args:
        date_string (str): string with the format '%Y-%m-%dT%H:%M:%S.%fZ'
    Returns:
        datetime:
    """
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')


def to_snake_case(name):
    """Converts a string into snake_case format"""
    name = name.replace('-', '_')
    temp = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', temp).lower()


def extract_type(obj):
    """Get the name of a Python object, based on its type

    Args:
        obj (object): Python object
    Returns:
        str:
    """
    pattern = re.compile(r"^<class '(?P<obj_type>[.a-zA-Z/_]*)'>$")
    match = pattern.match(str(type(obj)))
    ans = match.group('obj_type') if match else str(type(obj))
    translator = dict(NoneType='None')
    ans = ans.split(".")[-1]
    return translator.get(ans, ans)


def dumps_datetime(date):
    """Datetime into string"""
    if isinstance(date, datetime):
        return date.__str__()
    return None


def parse_image_url(image_url):
    """Parse the image filename using a regular expression.

    Args:
        image_url (string): url which must be parsed
    Returns:
        tuple (str or None): filename and format got from the filename.
        If it doesn't match, returns a None tuple.
    """
    path = urlparse(image_url).path
    pattern = re.compile(
        r'/(?P<filename>[0-9a-zA-Z_-]*).(?P<format>[a-z0-9]{3,4})$'
    )
    match = pattern.search(path)
    if match:
        return match.group('filename'), match.group('format')
    return None, None


def dict_to_tsv(data):
    """Get a pretty representation of a dictionary as a table.

    Args:
        data_error (dict):
    Returns:
        str: pretty representation of the dictionary ``data``
    """
    offset = max([len(item) for item in data.keys()]) + 3

    def multiline(long_string):
        """Wraps a string and add some indentation to lines (except
        for the first one).

        Args:
            long_string (str): string to wrap
        Returns:
            str: string wrapped.
        """
        multilines = textwrap.wrap(long_string, width=70)
        multilines = [
            int(index > 0) * offset * ' ' + item
            for index, item in enumerate(multilines)
        ]
        return "\n".join(multilines)

    template = []
    for item in data:
        multilined = multiline(str(data[item]))
        template.append("{label:{offset}}{text}".format(
            label=item, text=multilined, offset=offset))
    return "\n".join(template)
