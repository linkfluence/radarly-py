"""
.. _API call: https://api.linkfluence.com/officialdoc/architecture/project.html#get-project-infos

As in Radarly, the ``Project`` object contains all the needed data
in order to start exploring a project. The ``Project`` object is built
dynamically using the response got from the `API call`_ in order to retrieve
information about a project. Several methods have been defined in order
to, for example, retrieve publications inside the project, know the
influencers or get some statitics about publications inside your project.
"""

from .analytics import Analytics
from .api import RadarlyApi
from .benchmark import Benchmark
from .cloud import Cloud
from .cluster import Cluster
from .corpus import InfoCorpus
from .dashboard import Dashboard
from .distribution import Distribution
from .focus import Focus
from .geogrid import GeoGrid
from .influencer import Influencer
from .localization import Localization
from .milestone import Milestone
from .model import SourceModel
from .pivottable import PivotTable
from .publication import Publication
from .socialaccount import SocialAccount
from .socialperformance import SocialPerformance
from .tag import Tag
from .topic import Entities, TopicWheel
from .utils._internal import id_to_value, instance_builder


class Project(SourceModel):
    """Object to explore a project in Radarly. This object is made
    dynamically but you can explore it using the methods defined in
    ``SourceModel``.

    Example:

        >>> project.keys()
        {'id', 'account_id', 'label', ..., 'brand_logos'}
        >>> project.draw_structure(max_depth=1)
        Project (Project)
         | id (str)
         | doc_count (int)
         ...
        >>> project['tags']
        [<Tag.id=xxxx.type=user>, <Tag.id=xxxx.type=custom>, ...]
        >>> project['$.tags(type=custom).subtags']
        ...

    Here is information about some useful attributes of the ``Project``
    object.

    Args:
        id (string): the unique ID used in our database to identify the project
        docs_count (int): the actual number of documents inside your project
        created (datetime.datetime): creation date of the project
        updated (datetime.datetime): last date the project was updated
        focuses (Focuses): list of all focuses (queries) of the project
        dashboards (Dashboards): list of all dashboards created to organize your
            project.
        tags (Tags): list of all tags of the project
        social_accounts (dict): information about the social accounts
            registred in your project.
        benchmark_entities (list[dict]): information about the accounts
            available for a benchmark
    """

    def __init__(self, data, translator=None, api=None):
        base_translator = dict(
            tags=Tag._builder,
            dashboards=Dashboard._builder,
            focuses=Focus._builder,
            milestones=Milestone._builder,
            social_accounts=SocialAccount._builder,
            corpora=InfoCorpus._builder
        )
        translator = translator or dict()
        base_translator.update(translator)
        super().__init__(data, base_translator)
        api = api or RadarlyApi.get_default_api()

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
        Get information about a specific project.

        Args:
            pid (int): project id of the project
            api (RadarlyApi, optional): api which must be used to perform the
                request. If ``None``, the default API will be used.
        Returns:
            Project:
        """
        api = api or RadarlyApi.get_default_api()
        project = api.get(api.router.project['find'].format(project_id=pid))
        return cls(project, api=api)

    def get_distribution(self, parameter, api=None):
        """
        Get distribution of volume, reach, engagement actions
        or/and impressions on a set of publications.

        Args:
            parameter (DistributionParameter): parameter used to specify
                on which subset of publications the distribution must be
                computed and how the distribution must be computed.
                See ``DistributionParameter`` documentation to see
                how to build this object.
            api (RadarlyApi, optional): api which must be used to perform the
                request. If ``None``, the default API will be used.
        Returns:
            Distribution: a list-like object storing all data about the asked
            distribution. You can use the ``pandas`` module to explore this
            object.
        """
        return Distribution.fetch(
            getattr(self, 'id'), parameter, api=api
        )

    def get_publications(self, parameter, api=None):
        """
        Get publications of your project.

        Args:
            parameter (SearchPublicationParameter): parameters object
                made with ``SearchPublicationParameter`` object, which will
                be used as payload data in the POST request to retrieve
                publications.
            api (RadarlyApi, optional): api which must be used to perform the
                request. If ``None``, the default API will be used.
        Returns:
            list[Publication]:
        """
        return Publication.fetch(
            getattr(self, 'id'), parameter, api
        )

    def get_all_publications(self, parameter, api=None):
        """Get all publications matching given parameters. It returns a
        generator which yields publications.

        Args:
            parameter (SearchPublicationParameter): parameters object
                made with the SearchPublicationParameter instance, which will
                be used as payload data in POST request. Go to
                ``SearchPublicationParameter`` documentation to know how to
                build this object.
            api (RadarlyApi, optional): api which must be used to perform the
                request. If ``None``, the default API will be used.
        Returns:
            PublicationGenerator: generator of publications. On each iterations, a
            Publication is yielded until there is no more publication.
        """
        return Publication.fetch_all(
            getattr(self, 'id'), parameter, api
        )

    def get_influencers(self, parameter, api=None):
        """Get influencers linked to a project.

        Args:
            parameter (InfluencerParameter): parameter sent as payload
                to the API. Go to ``InfluencerParameter`` documentation to see
                how to build this object.
            api (RadarlyApi, optional): api which must be used to perform the
                request. If ``None``, the default API will be used.
        Returns:
            list[Influencer]:
        """
        return Influencer.fetch(
            getattr(self, 'id'), parameter, api
        )

    def get_all_influencers(self, parameter, api=None):
        """Get all influencers in a project matching some parameters.

        Args:
            parameter (InfluencerParameter): parameters object which
                is the payload of the request made to get data. Must contains
                pagination's parameter.
            api (RadarlyApi, optional): api which must be used to perform the
                request. If ``None``, the default API will be used.
        Returns:
            InflencersGenerator: generator which yields influencer
        """
        return Influencer.fetch_all(
            getattr(self, 'id'), parameter, api=api
        )

    def get_analytics(self, parameter, api=None):
        """Retrieve some statistics from the API. It allows you to dive deeper
        into the analysis of your publication's project by retrieving several
        kind of analytics, computed on all or a subset of the publications
        stored in your project.

        Args:
            parameter (AnalyticsParameter): parameter used to specify
                which analytics you want to compute, on which subset of
                publications to work... See ``AnalyticsParameter``
                documentation to get some help on how build this object.
            api (RadarlyApi, optional): api which must be used to perform the
                request. If ``None``, the default API will be used.
        Returns:
            Analytics: object storing data retrieved from the API. Each field
            can be explored with ``pandas``.
        """
        focuses = id_to_value(getattr(self, 'focuses'), 'focuses')
        return Analytics.fetch(getattr(self, 'id'), parameter,
                               focuses=focuses, api=api)

    def get_localizations(self, parameter, api=None):
        """Get geographical distribution by region or town.

        Args:
            parameter (LocalizationParameter): object sent as payload to
                the API. Go to ``LocalizationParameter`` documentation to
                know how to build this object.
            api (RadarlyApi, optional): api which must be used to perform the
                request. If ``None``, the default API will be used.
        Returns:
            Localization: list of statistics by geographical point
        """
        return Localization.fetch(getattr(self, 'id'), parameter,
                                  api=api)

    def get_cloud(self, parameter, api=None):
        """Retrieve cloud statistics from the Radarly API.

        Args:
            parameter (CloudParameter): parameter used to
                specify on which subset of publications the cloud
                computations must be performed and which key must
                be returned. Go to ``CloudParameter`` documentation
                to know how you can build this object.
        Returns:
            Cloud: dict-like object storing statistics by fields
        """
        return Cloud.fetch(getattr(self, 'id'), parameter, api)

    def get_pivot_table(self, parameter, api=None):
        """Retrieve data from the API in order to build the pivot table object.

        Args:
            parameter (PivotParameter): parameter used to restrict the set
                of publications on which the pivot table will be based.
                Go to ``PivotParameter`` documentation to see how to build
                this object.
            api (RadarlyApi, optional): api which must be used to perform the
                request. If ``None``, the default API will be used.
        Returns:
            PivotTable: data from the pivot table. You can use ``pandas`` to
            interact with it.
        """
        focuses = id_to_value(getattr(self, 'focuses'), 'focuses')
        fields = id_to_value(getattr(self, 'tags'), 'tags')
        return PivotTable.fetch(getattr(self, 'id'), parameter,
                                focuses=focuses, fields=fields, api=api)

    def get_social_performance(self, parameter, api=None):
        """Retrieve information about social account performance from the API.

        Args:
            parameter (SocialPerformanceParameter): object sent as
                payload to the API. Go to ``SocialPerformanceParameter`` to
                know how to build this object.
            api (RadarlyApi, optional): api which must be used to perform the
                request. If ``None``, the default API will be used.
        Returns:
            SocialPerformance: list-like object compatible with ``pandas``
        """
        return SocialPerformance.fetch(getattr(self, 'id'), parameter,
                                       api=api)

    def get_benchmark(self, parameter, api=None):
        """Retrieve benchmark information from the Radarly API.

        Args:
            parameter (BenchmarkParameter): parameter used to configure
                the benchmark which will be performed. Go to
                ``BenchmarkParameter`` documentation to see how you can
                build this object.
            api (RadarlyApi, optional): api which must be used to perform the
                request. If ``None``, the default API will be used.
        Returns:
            Benchmark: dict-like object storing benchmark data by platform
        """
        return Benchmark.fetch(getattr(self, 'id'), parameter,
                               api=api)

    def get_topic_and_entity(self, parameter, api=None):
        """
        Get distribution by category and subcategory.

        Args:
            parameter (TopicParameter): parameter sent as payload
                to the API. Go to ``TopicParameter`` documenation to know
                how to build this object.
            api (RadarlyApi, optional): api which must be used to perform the
                request. If ``None``, the default API will be used.
        Returns:
            TopicWheel, Entities:
        """
        api = api or RadarlyApi.get_default_api()
        param = parameter.copy()
        url = api.router.topicwheel['fetch'].format(
            project_id=getattr(self, 'id')
        )
        url = url + '?locale={}'.format(param.pop('locale'))
        res_data = api.post(url, data=param)
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

    def get_geogrid(self, parameter, api=None):
        """retrieve geographical distribution from the API.

        Args:
            parameter (GeoParameter): parameter to specify how to
                compute the geographical distribution. Go to ``GeoParameter``
                documentation to know how to build this object.
            api (RadarlyApi, optional): api which must be used to perform the
                request. If ``None``, the default API will be used.
        Returns:
            GeoGrid: list-like object compatible with ``pandas``
        """
        return GeoGrid.fetch(getattr(self, 'id'), parameter,
                             api=api)

    def get_clusters(self, parameter, api=None):
        """Retrieve clusters from the Radarly API.

        Args:
            parameter (ClusterParameter): parameter to configure
                how the cluster are built and which subet of publications must
                be used. Go to ``ClusterParameter`` documentation to know how
                to build this object.
            api (RadarlyApi, optional): api which must be used to perform the
                request. If ``None``, the default API will be used.
        Returns:
            Cluster: cluster object
        """
        return Cluster.fetch(getattr(self, 'id'), parameter,
                             api=api)


class InfoProject(SourceModel):
    """Object storing information about a project (but not all available
    information). To get the full version of the object, you can use the
    ``expand`` class method.
    """
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
        """Retrieve additional information about a project from the API.

        Args:
            api (RadarlyApi, optional): API used to perform the request.
                If ``None``, the default API will be used.
        Returns:
            Project: object storing all available information about a project
        """
        api = api or RadarlyApi.get_default_api()
        return Project.find(pid=getattr(self, 'id'), api=api)
