"""
Radarly can compute some statistics and then group the result by countries or
town. The ``localization`` modules defines all objects in order to interact
with such results.
"""

import copy

from .api import RadarlyApi
from .utils.misc import to_snake_case


class Localization(list):
    """List-like object used to store data about the geographical
    distribution. Each item of the distribution is a dictionary of statistics
    about a specific localization. This object is compatible with ``pandas``,
    so you convert it to a DataFrame:

    >>> import pandas as pd
    >>> localizations
    Localization(length=100)
    >>> pd.DataFrame(localizations).head()
          doc                 id              idStr isoCode lang       lat  \\
    0   20963  72057594041390308  72057594041390308   BR-GO   en -15.58071
    1   38483  72057594043029696  72057594043029696   US-NJ   en  40.16706
    2  551932  72057594044197067  72057594044197067  GB-ENG   en  52.16045
    3   16393  72057594042289821  72057594042289821   US-MD   en  39.00039
    4   35604  72057594040566296  72057594040566296  GB-SCT   en  56.00000
    ...
    """
    def __init__(self, data):
        super().__init__()
        for item in (i for i in data):
            element = item['counts']
            element.update(item['info'])
            del item['counts']
            del item['info']
            element.update(item)
            self.append(element)

    def __repr__(self):
        return '<Localization.length={}>'.format(len(self))

    @classmethod
    def fetch(cls, project_id, parameter, api=None):
        """Get geographical distribution by country or town.

        Args:
            project_id (int): identifier of your project
            parameter (LocalizationParameter): object sent as payload to
                the API. See ``LocalizationParameter`` on how to build this
                object.
            api (RadarlyApi, optional): API used to make the
                request. If None, the default API will be used.
        Returns:
            Localization: list of stats by geographical point
        """
        parameter = copy.deepcopy(parameter)
        api = api or RadarlyApi.get_default_api()
        url = api.router.localization['fetch'].format(
            project_id=project_id,
            region_type=parameter.pop('geo_type', 'region')
        )
        params = [
            ('locale', parameter.pop('locale', 'en_GB'))
        ]
        data = api.post(url, params=params, data=parameter)
        return cls(data[to_snake_case('geo-digging')])
