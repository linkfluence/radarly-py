"""
Some functions and classes used internally.
"""

from .misc import flat


def instance_builder(cls, data, *args, **kwargs):
    """Build an object of a specific class. Scalable (if a list
    is set as argument, return a list of object; else just one object)
    """
    if not data:
        return data
    elif isinstance(data, dict):
        return cls(data, *args, **kwargs)
    elif isinstance(data, list):
        return [cls(item, *args, **kwargs) for item in data]
    raise TypeError


class CallableDict(dict):
    """Dict which return the key if it was not found. It also try to convert
    the key into an integer"""
    def __missing__(self, key):
        try:
            key = int(key)
        except KeyError:
            pass
        if key in self:
            return self[key]
        return str(key)

    def __call__(self, key):
        return self[key]


def id_to_value(data, dtype):
    """Based on some datas, build a dictionary to translate an ID to a
    a label"""
    if dtype == 'focuses':
        return dict([
            (focus['id'], focus['label']) for focus in data
        ])
    elif dtype == 'tags':
        return dict(flat([[
            (subtag['id'], subtag['value']) for subtag in tag.subtags
        ] for tag in data]))
    raise ValueError


def parse_struct_stat(stats):
    """Parse the structure of stats values in influencer data in order
    to return a pandas-compatible object.
    """
    data = dict()
    for stat in stats:
        for item in stats[stat]:
            for metric in item['counts']:
                data.setdefault(metric, dict())
                data[metric].update({
                    (stat, item['term']): item['counts'][metric]
                })
    return data


def parse_struct_interval(intervals):
    """Parse the response to get distribution which can be easily converted
    with pandas"""
    data = dict()
    for item in intervals:
        for metric in item['counts']:
            data.setdefault(metric, {})
            data[metric].update({item['date']: item['counts'][metric]})
    return data
