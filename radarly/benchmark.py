"""
In Radarly, the benchmark feature allows you to compare your own social media
accounts with those of your competitors. Thanks to that, you can manage and
measure the performance of your accounts.
This module defines the Python object used to store the data of this
benchmark.
"""

from .api import RadarlyApi


class Benchmark(dict):
    """Dict-like object used to store the benchmark data. The keys of this
    object are the available platforms on which the different social accounts
    have been compared. The value associated to each platform is an object
    which can be transformed into a ``pandas.DataFrame`` for a better
    exploration.

    Example:

        >>> benchmark
        Benchmark(platforms=['facebook', 'instagram'])
        >>> import pandas as pd
        >>> pd.DataFrame(benchmark['facebook'])
    """

    def __init__(self, data):
        super().__init__()
        for platform in data:
            self[platform] = []
            for account in data[platform]:
                for stat in account['stats']:
                    item = {'date': stat['date']}
                    item.update(stat['scores'])
                    item.update({'account_id': account['uid']})
                    item['platform'] = platform
                    self[platform].append(item)

    def __repr__(self):
        return '<Benchmark.platforms={}>'.format(list(self.keys()))

    @classmethod
    def fetch(cls, project_id, parameter, api=None):
        """Retrieve benchmark information from the Radarly API.

        Args:
            project_id (int): identifier of your project where information is
                stored
            parameter (BenchmarkParameter): parameter used to configure
                the benchmark which will be performed. See the documentation
                of ``BenchmarkParameter`` to see how you can build this object.
            api (RadarlyApi, optional): API object used to perform the request.
                If None, it will use the default API.
        Returns:
            Benchmark: dict-like object storing benchmark data by platform
        """
        api = api or RadarlyApi.get_default_api()
        url = api.router.benchmark['fetch'].format(project_id=project_id)
        data = api.get(url, params=parameter)
        return cls(data)
