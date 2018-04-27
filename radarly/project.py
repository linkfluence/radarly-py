"""
.. _API call: /officialdoc/architecture/project.html#get-project-infos

As in Radarly, the ``Project`` object contains all the needed data
in order to start exploring a project. The ``Project`` object is made
dynamically using the response get from the `API call`_ to get all
informations about a project. Several methods have been defined in order
to get informations and make some computations inside your project.
"""

from .api import RadarlyApi
from .benchmark import Benchmark
from .cloud import Cloud
from .cluster import Cluster
from .dashboard import Dashboard
from .distribution import Distribution
from .focus import Focus
from .geogrid import GeoGrid
from .influencer import Influencer, InfluencersGenerator
from .localization import Localization
from .model import SourceModel
from .pivottable import PivotTable
from .publication import Publication
from .socialaccount import SocialAccount
from .socialperformance import SocialPerformance
from .analytics import Analytics
from .tag import Tag
from .topic import Entities, TopicWheel
from .utils.router import Router
from .utils._internal import id_to_value, instance_builder


class Project(SourceModel):
    """Object to explore a project in Radarly. This object is made
    dynamically but you can explore it using the methods inherited
    from ``SourceModel``.

    Example:

        >>> project.keys()
        dict_keys(['id', 'account_id', 'label', ..., 'brand_logos'])
        >>> project.draw_structure(max_depth=1)
        Project (Project)
         | id (str)
         | doc_count (int)
         ...
        >>> project['tags']
        [<Tag.id=xxxx.type=user>, <Tag.id=xxxx.type=custom>, ...]
        >>> project['$.tags.subtags']
        ...

    Here are informations about some useful keys of the ``Project`` object.

    Args:
        id (string): the unique ID used in our database to identify the project
        doc_count (int): the actual number of documents related to the project
        created (datetime.datetime): creation date of the project
        updated (datetime.datetime): last datetime the project has been updated
        focuses (Focuses): list of all focuses (queries) of the project
        dahboards (Dashboards): list of all dashboards created to organize your
            project.
        tags (Tags): list of all tags of the project
        social_accounts (dict): informations about the social accounts
            regitred in your project.
        benchmark_entities (list[dict]): informations about the accounts
            available for a benchmark
    """

    def __init__(self, data, translator=None, api=None):
        base_translator = dict(
            tags=Tag._builder,
            dashboards=Dashboard._builder,
            focuses=Focus._builder,
            social_accounts=SocialAccount._builder
        )
        translator = translator or dict()
        base_translator.update(translator)
        super().__init__(data, base_translator)
        self._api = api or RadarlyApi.get_default_api()

    def __repr__(self):
        pid, label = getattr(self, 'id'), getattr(self, 'label')
        return '<Project.pid={}.label={}>'.format(pid, label)

    @classmethod
    def _builder(cls, data):
        """Make a list of project object from a list of project's data"""
        return instance_builder(cls, data)

    @classmethod
    def find(cls, pid, api=None):
        """
        Get informations about a specific project.

        Args:
            pid (int): project id of the project
            api (RadarlyApi, optional): api which must be used to perform the
                request. If None, the default API will be used.
        Returns:
            Project:
        """
        api = api or RadarlyApi.get_default_api()
        project = api.get(Router.project['find'].format(project_id=pid))
        return cls(project, api=api)

    def _fetch_with_post(self, url, param_obj):
        return self._api.post(url, data=param_obj)

    def get_distribution(self, search_parameter):
        """
        Get distribution of volume, reach, engagement actions
        or/and impressions on a set of publications.

        Args:
            search_parameter (DistributionParameter): parameter used to specify
                on which subset of publications the distribution must be
                computed. See ``DistributionParameter`` documentation to see
                how to build this object.
        Returns:
            Distribution: a list-like object storing all datas about the wanted
            distribution. You can use the `pandas` module in order to
            easily explore this object.
        """
        return Distribution.fetch(
            getattr(self, 'id'), search_parameter, api=self._api
        )

    def get_publications(self, search_parameter):
        """
        Get publications linked to a project.

        Args:
            search_parameter (SearchPublicationParameter): parameters object
                made with the SearchPublicationParameter instance, which will
                be used as payload data in POST request.
        Returns:
            list[Publication]:
        """
        return Publication.fetch(
            getattr(self, 'id'), search_parameter, self._api
        )

    def get_all_publications(self, search_parameter):
        """Get all publications matching given parameters. It returns a
        generator which yields publications.

        Args:
            search_parameter (SearchPublicationParameter): parameters object
                made with the SearchPublicationParameter instance, which will
                be used as payload data in POST request. See
                ``SearchPublicationParameter`` to know how to build this object
        Returns:
            PublicationGenerator: generator of publications. On each iterations, a
            Publication is yielded until there is no more publications.
        """
        return Publication.fetch_all(
            getattr(self, 'id'), search_parameter, self._api
        )

    def get_influencers(self, search_parameter):
        """Get influencers linked to a project.

        Args:
            search_parameter (InfluencerParameter): parameter sent as payload
                to the API. See ``InfluencerParameter`` to see how to build
                this object.
        Returns:
            list[Influencer]:
        """
        return Influencer.fetch(
            getattr(self, 'id'), search_parameter, self._api
        )

    def get_all_influencers(self, search_parameter):
        """Get all influencers in a project matching some parameters.

        Args:
            search_parameter (InfluencerParameter): parameters object which
                is the payload of the request made to get datas. Must contains
                pagination's parameter.
        Returns:
            InflencersGenerator: generator which yields influencer
        """
        return InfluencersGenerator(
            getattr(self, 'id'), search_parameter, api=self._api
        )

    def get_analytics(self, search_parameter):
        """Retrieve some insights from the API. It allows you to dive deeper
        into the analysis of your project by retrieving several kind of
        analytics computed on all publications stored in your project (eg
        **tones** or **gender**).

        Args:
            search_parameter (AnalyticsParameter): parameter used to specify
                which analytics you want to compute, on which subset of
                publications to work... See ``AnalyticsParameter``
                documentation to get some help on how build this object.
        Returns:
            Analytics: object storing datas retrieved from the API and which
            can be explore with ``pandas``
        """
        focuses = id_to_value(getattr(self, 'focuses'), 'focuses')
        return Analytics.fetch(getattr(self, 'id'), search_parameter,
                               focuses=focuses, api=self._api)

    def get_localizations(self, search_parameter):
        """Get geographical distribution by country or town.

        Args:
            search_parameter (LocalizationParameter): object send as payload to
                the API. See ``LocalizationParameter`` on how to build this
                object.
        Returns:
            Localization: list of stats by geographical point
        """
        return Localization.fetch(getattr(self, 'id'), search_parameter,
                                  api=self._api)

    def get_cloud(self, search_parameter):
        """Retrieve cloud informations from the Radarly's API.

        Args:
            search_parameter (CloudParameter): parameter used to
                specify on which subset of publications the cloud
                computations must be performed and which key must
                be returned. See ``CloudParameter`` documentation
                to know how you can build this object.
        Returns:
            Cloud: dict-like object storing statistics by fields
        """
        return Cloud.fetch(getattr(self, 'id'), search_parameter, self._api)

    def get_pivot_table(self, pivot_parameter):
        """Retrieve data from the API in order to build the pivot table object.

        Args:
            search_parameter (PivotParameter): parameter used to restrict data
                used to build the pivot table. See ``PivotParameter``
                documentation to see how to build this object.
        Returns:
            PivotTable: data from the pivot table. You can use ``pandas`` to
            interact with it
        """
        focuses = id_to_value(getattr(self, 'focuses'), 'focuses')
        fields = id_to_value(getattr(self, 'tags'), 'tags')
        return PivotTable.fetch(getattr(self, 'id'), pivot_parameter,
                                focuses=focuses, fields=fields, api=self._api)

    def get_social_performance(self, search_parameter):
        """Retrieve informations about social account performance from the API.

        Args:
            search_parameter (SocialPerformanceParameter): object sent as
                payload to the API. See ``SocialPerformanceParameter`` to see
                how to build this object.
        Returns:
            SocialPerformance: list-like object compatible with ``pandas``
        """
        return SocialPerformance.fetch(getattr(self, 'id'), search_parameter,
                                       api=self._api)

    def get_benchmark(self, search_parameter):
        """Retrieve benchmark informations from the Radarly's API.

        Args:
            search_parameter (BenchmarkParameter): parameter used to configure
                the benchmark which will be performed. See the documentation
                of ``BenchmarkParameter`` to see how you can build this object.
        Returns:
            Benchmark: dict-like object storing benchmark datas by platform
        """
        return Benchmark.fetch(getattr(self, 'id'), search_parameter,
                               api=self._api)

    def get_topic_and_entity(self, search_parameter):
        """
        Get distribution by category and subcategory.

        Args:
            search_parameter (TopicParameter): parameter sent as payload
                to the API. See ``TopicParameter`` to see how to build
                this object.
        Returns:
            TopicWheel, Entities:
        """
        param = search_parameter.copy()
        url = Router.topicwheel['fetch'].format(project_id=getattr(self, 'id'))
        url = url + '?locale={}'.format(param.pop('locale'))
        res_data = self._fetch_with_post(url, param)
        categories = []
        entities = []

        for topic in res_data['topics']:
            category = topic['category']
            terms = category.pop('term').split('.')
            category['category'], category['subcategory'] = terms
            category.update(category.pop('counts'))
            categories.append(category)
            for entity in topic['entity']:
                entity.update(entity.pop('counts'))
                entity['category'], entity['subcategory'] = terms
                entities.append(entity)
        categories.sort(key=lambda x: x['category'])
        entities.sort(key=lambda x: x['category'])

        return TopicWheel(categories), Entities(entities)

    def get_geogrid(self, search_parameter):
        """Retrive geographical distribution from the API.

        Args:
            search_parameter (GeoParameter): parameter to specify how to
                compute the geographical distribution. See ``GeoParameter``
                documentation to see how to build this object.
        Returns:
            GeoGrid: list-like object compatible with ``pandas``
        """
        return GeoGrid.fetch(getattr(self, 'id'), search_parameter,
                             api=self._api)

    def get_clusters(self, search_parameter):
        """Retrieve clusters from the Radarly's API.

        Args:
            search_parameter (ClusterParameter): parameter to configure
                how the cluster are calculated. See ``ClusterParameter``
                documentation to know how build this object.
        Returns:
            Cluster: cluster object
        """
        return Cluster.fetch(getattr(self, 'id'), search_parameter,
                             api=self._api)


class InfoProject(SourceModel):
    """Some informations about a project"""
    def __init__(self, data, translator=None):
        super().__init__(data, translator=translator)

    def __repr__(self):
        pid, label = getattr(self, 'id'), getattr(self, 'label')
        return '<InfoProject.pid={}.label={}>'.format(pid, label)

    @classmethod
    def _builder(cls, data):
        """Make a list of project object from a list of project's data which
        yields project object"""
        return [cls(item) for item in data]

    def expand(self, api=None):
        """Retrieve all informations about a project from the API.

        Args:
            api (RadarlyApi): API used to perform the request. If None,
                the default API will be used.
        Returns:
            Project:
        """
        api = api or RadarlyApi.get_default_api()
        return Project.find(pid=getattr(self, 'id'), api=api)
