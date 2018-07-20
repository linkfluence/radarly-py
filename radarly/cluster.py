"""A cluster in Radarly is a set of publications grouped by strong
similarities (for example, articles published in several medias but
with the same source will be grouped in the same cluster)."""

from copy import deepcopy
from reprlib import repr as truncate_repr

from .analytics import Analytics
from .api import RadarlyApi
from .model import SourceModel
from .publication import Publication
from .cloud import Cloud


class Cluster(SourceModel):
    """Object which inherits from the ``SourceModel`` storing information
    about a cluster"""
    def __init__(self, data, api=None):
        self._api = api or RadarlyApi.get_default_api()
        del data['stats']
        super().__init__(data)

    def __repr__(self):
        return '<Cluster.size={}.story={}>'.format(
            getattr(self, 'size'), truncate_repr(getattr(self, 'story'))
        )

    @classmethod
    def fetch(cls, project_id, parameter, api=None):
        """Retrieve clusters from the Radarly API.

        Args:
            project_id (int): identifier of your project
            parameter (ClusterParameter): parameter to configure
                how the cluster are calculated. See ``ClusterParameter``
                documentation to know how build this object.
            api (RadarlyApi, optional): API used to perform the
                request. If None, the default API will be used.
        Returns:
            Cluster: cluster object (you can the ``draw_structure`` to
                get its structure)
        """
        api = api or RadarlyApi.get_default_api()
        url = api.router.cluster['fetch'].format(project_id=project_id)
        data = api.post(url, data=parameter)
        ans = []
        for data in data['hits']:
            data['project_id'] = project_id
            ans.append(cls(data, api=api))
        return ans

    def get_analytics(self, parameter, focuses=None):
        """Compute some insights about the set of publications in the
        cluster.

        Args:
            parameter (AnalyticsParameter): object sent as payload to the
                API to configure insights computation. See
                ``AnalyticsParameter`` documentation to see how build this
                object.
            focuses (dict, optional): dictionary used to translate focuses
                if 'focuses' was asked as field
        Returns:
            Analytics:
        """
        parameter = deepcopy(parameter)
        parameter['stories'] = [getattr(self, 'story')]
        return Analytics.fetch(getattr(self, 'project_id'), parameter,
                               focuses=focuses, api=self._api)

    def get_publications(self, parameter):
        """Retrieve publications in the cluster.

        Args:
            parameter (SearchPublicationParameter): object sent as payload to
                the API to configure insights computation. See
                ``SearchPublicationParameter`` documentation to see how to
                build this object.
        Returns:
            Analytics:
        """
        parameter = deepcopy(parameter)
        parameter['stories'] = [getattr(self, 'story')]
        return Publication.fetch(
            getattr(self, 'project_id'), parameter, self._api
        )

    def get_cloud(self, parameter):
        """Retrieve clouds insights about publications in the cluster.

        Args:
            parameter (CloudParameter): object sent as payload to the API. See
                ``CloudParameter`` documentation to see how to build this
                object.
        Returns:
            Cloud:
        """
        parameter = deepcopy(parameter)
        parameter['stories'] = [getattr(self, 'story')]
        return Cloud.fetch(
            getattr(self, 'project_id'), parameter, self._api
        )
