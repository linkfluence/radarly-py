"""
The aim of this module is to give you the possibility to make some
computations on your publications. Each analytics is returned as a time
distribution of some metrics.

.. note:: Each time you try to retrieve some analytics, the Radarly's server
    launch some computation tasks, hence the loading time which can reach
    several seconds.
"""

from .api import RadarlyApi
from .constants import ANALYTICS_FIELD
from .utils._internal import CallableDict


class Analytics(dict):
    """Dict-like object. Each key gives access to a specific kind of
    statistics (asked in the parameter in the *fields* key).
    This object can be explored with ``pandas``.

    >>> import pandas as pd
    >>> stats
    Analytics(fields=['occupations', 'languages', ..., 'logos', 'genders'])
    >>> languages = pd.DataFrame(stats['languages'])
    >>> languages.head()
                    af   ar  ar-bz  bg  bn  ca  cs   da  de  dv  ...     th  \\
    doc 2018-01-01 NaN   79    1.0   9 NaN  11   6  NaN  22 NaN  ...    214
        2018-01-02 NaN  199    NaN  30 NaN   6   6  7.0  27 NaN  ...    275
        2018-01-03 NaN  132    1.0  13 NaN   4   3  1.0  40 NaN  ...    207
        2018-01-04 NaN  109    NaN  10 NaN   5   3  7.0  43 NaN  ...    212
        2018-01-05 NaN   83    NaN  13 NaN   9   6  8.0  36 NaN  ...    206
    ...

    Args:
        fields: fields currently stored in the Analytics objects. Each value
            associated to a field can be transformed to a DataFrame.
    """
    def __init__(self, data, focuses=None):
        super().__init__()
        focuses = (lambda x: x) if focuses is None else CallableDict(focuses)
        translator = dict(
            focuses=focuses
        )
        self.setdefault('total', {'total': {}})
        self.setdefault('counts', {})
        for dot in data['dots']:
            dot_date = dot['date']

            self['total']['total'][dot_date] = dot['total']
            for major in dot['counts'].keys():
                self['counts'].setdefault(major, {})
                self['counts'][major][dot_date] = dot['counts'][major]

            _ = [self.setdefault(key, {}) for key in dot['stats'].keys()]

            for major in dot['stats'].keys():
                temp = {
                    translator.get(major, lambda x: x)(item['term']): {
                        (metric, dot_date):
                            item['counts'][metric]
                        for metric in item['counts']
                    } for item in dot['stats'][major]
                }
                for field in temp:
                    if not str(field).startswith('tag_offset_'):
                        self[major].setdefault(field, {})
                        self[major][field].update(temp[field])

        self.fields = list(self.keys())

    def __repr__(self):
        return '<Analytics.fields={}>'.format(list(self.keys()))

    @classmethod
    def fetch(cls, project_id, parameter,
              focuses=None, api=None):
        """Retrieve some insights from the API. It allows you to dive deeper
        into the analysis of your project by retrieving several kind of
        analytics, computed on all or a subset of the publications stored in
        your project.

        Args:
            project_id (int): id of your project where all data are stored
            parameter (AnalyticsParameter): parameter used to specify
                which analytics you want to compute, on which subset of
                publications to work... See ``AnalyticsParameter``
                documentation to get some help on how build this object.
            focuses (dict): used to translate headers if *focuses* was asked
                in the field.
            api (RadarlyApi, optional): API to use to made the request. If
                None, it will use the default API.
        Returns:
            Analytics: object storing data retrieved from the API and which
            can be explored with ``pandas``
        """
        api = api or RadarlyApi.get_default_api()
        url = api.router.analytics['global'].format(project_id=project_id)

        is_occupation_asked = ANALYTICS_FIELD.OCCUPATIONS in \
            parameter.get('fields', [])
        if is_occupation_asked:
            parameter['fields'].remove(ANALYTICS_FIELD.OCCUPATIONS)
        if parameter.get('fields', []) == [] and is_occupation_asked:
            data = dict(dots=[])
        else:
            data = api.post(url, data=parameter)
        if is_occupation_asked:
            _ = parameter.pop('fields')
            url = api.router.analytics['occupation'].format(
                project_id=project_id
            )
            occupations_data = api.post(url, data=parameter)
            data['dots'] += occupations_data['dots']

        return cls(data, focuses)
