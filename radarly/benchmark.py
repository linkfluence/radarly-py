"""
In Radarly, the benchmark feature allows you to compare your own social media
accounts with those of your competitors. Thanks to that, you can manage and
measure the performance of your accounts.
This module defines the Python's object used to store the data of this
benchmark.

.. warning:: This module will probably be change in order to allow you to have
    better interactions with the ``Benchmark`` object.
"""

from .api import RadarlyApi
from .utils.router import Router


class Benchmark(dict):
    """Dict-like object used to store the benchmark datas. The keys of this
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
        return '<Benchmark.platforms={}>'.format(self.keys())

    @classmethod
    def fetch(cls, project_id, search_parameter, api=None):
        """Retrieve benchmark informations from the Radarly's API.

        Args:
            project_id (int): identifier of your project in which
                informations are stored
            search_parameter (BenchmarkParameter): parameter used to configure
                the benchmark which will be performed. See the documentation
                of ``BenchmarkParameter`` to see how you can build this object.
            api (RadarlyApi, optional): API object used to perform the request.
                If None, it will be set to the default API.
        Returns:
            Benchmark: dict-like object storing benchmark datas by platform
        """
        api = api or RadarlyApi.get_default_api()
        url = Router.benchmark['fetch'].format(project_id=project_id)
        data = api.get(url, params=search_parameter)
        return cls(data)
