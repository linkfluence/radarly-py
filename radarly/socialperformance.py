"""
In Radarly, you can monitor the performance of any of your own social accounts.
This module defines an object in order to retrieve information about that.
"""

from .api import RadarlyApi


class SocialPerformance(list):
    """List-like object storing distribution over time of some stats about a
    social account. This object is compatible with ``pandas``.

    >>> social_perf
    <SocialPerformance.uid=172489456479180.platform=facebook>
    >>> import pandas as pd
    >>> df_social_perf = pd.DataFrame(social_perf)
    >>> df_social_perf.head()
                checkins  comments  count  global-brand-root-id  likes  \\
    date
    2018-03-14         0       NaN    1.0                 71773    576
    2018-03-15         0       4.0    NaN                 71773    643
    2018-03-16         0       1.0    1.0                 71773    807
    2018-03-17         0       4.0    1.0                 71773    574
    2018-03-18         0       4.0    1.0                 71773    510
    ...
    """
    def __init__(self, data, platform):
        super().__init__()
        self.uid = data['uid']
        self.platform = platform
        source = []
        for item in data['stats']:
            temp = {'date': item['date']}
            temp.update(item['scores'])
            source.append(temp)
        self.extend(source)

    def __repr__(self):
        return '<SocialPerformance.uid={0.uid}.platform={0.platform}>'.format(
            self
        )

    @classmethod
    def fetch(cls, project_id, parameter, api=None):
        """Retrieve information about social account performance from the API.

        Args:
            project_id (int): identifier of the project
            parameter (SocialPerformanceParameter): object sent as
                payload to the API. See ``SocialPerformanceParameter`` to see
                how to build this object.
            api (RadarlyApi, optional): API used to make the
                request. If None, the default API will be used.
        Returns:
            SocialPerformance: list-like object compatible with ``pandas``
        """
        api = api or RadarlyApi.get_default_api()
        platform = parameter['platform']
        parameter = parameter()

        url = api.router.social_performance['fetch'].format(
            project_id=project_id
        )
        url = "{}?{}".format(url, parameter)
        data = api.get(url)

        return [cls(item, platform) for item in data if item['stats']]
