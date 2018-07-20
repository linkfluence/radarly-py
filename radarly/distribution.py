"""
The distribution is a very useful feature in Radarly because it allows you
to get the distribution over time (by hour, day, week or month) of all your
publications.
"""

from .api import RadarlyApi


class Distribution(list):
    """
    List-like object storing the distribution over time of some metrics. Each item
    in the list is the statistics for one date. The ``Distribution`` object
    is compatible with ``pandas``.

    Example:

        >>> import pandas as pd
        >>> distribution
        Distribution(length=100)
        >>> df_distribution = pd.DataFrame(distribution)
        >>> df_distribution.set_index('date', inplace=True)
        >>> df_distribution.head()
                    doc  impression
        date
        2017-01-01  5678    55249194
        2017-01-02  6421    76283213
        2017-01-03  6489    69826116
        2017-01-04  7227    67470586
        2017-01-05  7646    68190331
    """
    def __init__(self, data):
        super().__init__()
        self.total = data['total']
        gen = (item for item in data['distribution'])
        for element in gen:
            temp = {'date': element['date']}
            temp.update(element['counts'])
            self.append(temp)

    def __repr__(self):
        return '<Distribution.length={}>'.format(len(self))

    @classmethod
    def fetch(cls, project_id, parameter, api=None):
        """Retrieve distribution data from the Radarly API.

        Args:
            project_id (int): identifier of your project
            parameter (DistributionParameter): parameter used to specify
                on which subset of publications the distribution must be
                computed. See ``DistributionParameter`` documentation to see
                how to build this object.
            api (RadarlyApi, optional): API used to make the
                request. If None, the default API will be used.
        Returns:
            Distribution: list-like object storing statistics by date.
        """
        api = api or RadarlyApi.get_default_api()
        url = api.router.distribution['fetch'].format(project_id=project_id)
        data = api.post(url, data=parameter)
        return cls(data['distribution'])
