"""
An influencer in Radarly is an author of several publications who has a
more-or-less large audience. The influencer module of ``radarly-py`` defines
several methods and functions in order to help you to understand who are the
influencers in your project and consequently understand your audience.
"""

from .api import RadarlyApi
from .model import GeneratorModel, SourceModel
from .utils._internal import parse_struct_stat


class Influencer(SourceModel):
    """Dict-like object storing information about an influencer. The value of
    this object are available as value associated to a key, or as attribute of
    the instance. Here are some useful attributes:

    .. warning:: The structure of the ``Influencer`` object may change
        depending on the platform

    Args:
        id (str): identifier for the influencer
        platform (str): origin platform of the influencer
        screen_name (str): display name on the social_accounts
        permalink (str): link to the social_account
        followers_count (int): numbers of followers of the influencer
        count (int): number of documents published by the follower in your
            project.
        stats (dict): statitics about the influencers publications
    """
    def __init__(self, data, project_id):
        self.project_id = project_id
        super().__init__()
        translator = dict(
            stats=parse_struct_stat
        )
        if 'user' in data:
            super().add_data(data['user'], translator)
            del data['user']
        super().add_data(data, translator)

    def __repr__(self):
        influ_id, platform = getattr(self, 'id'), getattr(self, 'platform')
        return '<Influencer.id={}.platform={}>'.format(influ_id, platform)

    @classmethod
    def find(cls, project_id, influencer_id, platform, api=None):
        """Retrieve information about an influencer.

        Args:
            project_id (int): id of the project
            influencer_id (int): id of the influencer
            platform (str): platform of the influencer
            api (RadarlyApi, optional): API used to make the
                request. If None, the default API will be used.
        Returns:
            Influencer:
        """
        api = api or RadarlyApi.get_default_api()
        url = api.router.influencer['find'].format(project_id=project_id)
        params = dict(
            uid=influencer_id,
            platform=platform
        )
        res_data = api.get(url, params=params)
        return Influencer(res_data, project_id)

    @classmethod
    def fetch(cls, project_id, parameter, api=None):
        """Retrieve influencers list from a project.

        Args:
            project_id (int): id of the project
            parameter (InfluencerParameter): parameter sent as payload
                to the API. See ``InfluencerParameter`` to see how to build
                this object.
            api (RadarlyApi): API used to performed the request. If None, the
                default API will be used.
        Returns:
            list[Influencer]:
        """
        api = api or RadarlyApi.get_default_api()
        url = api.router.influencer['search'].format(project_id=project_id)
        data = api.post(url, data=parameter)
        return [cls(item, project_id) for item in data['users']]

    @classmethod
    def fetch_all(cls, project_id, parameter, api=None):
        """retrieve all influencers from a project.

        Args:
            project_id (int): identifier of a project
            parameter (InfluencerParameter): parameter sent as payload
                to the API. See ``InfluencerParameter`` to see how to build
                this object. This object must contain pagination's parameters.
            api (RadarlyApi): API used to performed the request. If None, the
                default API will be used.
        Returns:
            InfluencerGenerator:
        """
        return InfluencersGenerator(parameter,
                                    project_id=project_id, api=api)

    def get_metrics(self, api=None):
        """Retrieve metrics data about the influencer from the API.

        Returns:
            dict:
        """
        api = api or RadarlyApi.get_default_api()
        params = dict(
            platform=self['platform'],
            uid=self['id']
        )
        url = api.router.influencer['find'].format(project_id=self.project_id)
        metrics = api.get(url, params=params)['metrics']
        return metrics


class InfluencersGenerator(GeneratorModel):
    """Generator which yields all influencers matching some payload.

    Args:
        search_param (InfluencerParameter):
        project_id (int):
        api (RadarlyApi):
    Yields:
        Influencer:
    """
    def _fetch_items(self):
        """Get next range of influencers"""
        url = self._api.router.influencer['search'].format(project_id=self.project_id)
        res_data = self._api.post(url, data=self.search_param)
        self.total = 1000
        self._items = (
            Influencer(item, self.project_id) for item in res_data['users']
        )
        div = self.total // self.search_param['limit']
        reste = self.total % self.search_param['limit']
        self.total_page = div
        if reste != 0: self.total_page += 1
        self.search_param = self.search_param.next_page()

    def __repr__(self):
        return '<InfluencersGenerator.total={}.total_page={}>'.format(
            self.total, self.total_page
        )
