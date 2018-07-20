"""
In Radarly, the cloud features is used to visualize the most relevant keywords,
hashtags, mentions, named entities... associated to your project or set of
publications.

The ``Cloud`` object in ``radarly`` is built to give you the possibility to retrieve
this kind of data.
"""

from .api import RadarlyApi


class Cloud(dict):
    """Dict-like object used to store the data of the cloud. The keys of this
    object corresponds to the differents statistics types available for the
    cloud (e.g *keywords*, *hashtags*, *mentions*,...). The value associated
    to each key of the ``Cloud`` object can easily be converted into a
    ``DataFrame``.

    Example:

        >>> import pandas as pd
        >>> cloud
        <Cloud.fields=['emojiCharts', 'mentions',... , 'hashtags', 'affects']>
        >>> mentions = pd.DataFrame(cloud['mentions'])
        >>> mentions
                            doc  impression     reach
        ABHcosmetics   10637    23040848   1843259
        BabyAnnie218       0      204310      8170
        BenefitBeauty   1997    16217028   1297354
        CHANEL          6207   706216524  56497312
        CHANELBEAUTY      34    48025113   1920999
    """
    def __init__(self, data):
        super().__init__()
        self.update(data)

    def __repr__(self):
        return '<Cloud.fields={}>'.format(list(self.keys()))

    @classmethod
    def fetch(cls, project_id, parameter, api=None):
        """Retrieve cloud data from the Radarly API.

        Args:
            project_id (int): identifier of your project.
            parameter (CloudParameter): parameter used to
                specify on which subset of publications the cloud
                computations must be performed and which key must
                be returned. See ``CloudParameter`` documentation
                to know how you can build this object.
            api (RadarlyApi, optional): API used to perform the
                request. If None, the default API will be used.
        Returns:
            Cloud: dict-like object storing statistics by fields
        """
        api = api or RadarlyApi.get_default_api()
        url = api.router.cloud['fetch'].format(project_id=project_id)
        data = api.post(url, data=parameter)
        return cls(data['cloud'])
