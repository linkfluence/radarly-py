"""
Parameters object sent as payload data.
"""

import json
from urllib.parse import urlencode

from .field import (ClusterMixin, FctxMixin, FieldsMixin, GeoFilterMixin,
                    GeoTypeMixin, IntervalMixin, LocaleMixin, MetricsMixin,
                    PaginationMixin, RangeDateMixin, SortMixin,
                    StandardParameterMixin, TimezoneMixin)

__all__ = (
    'AnalyticsParameter',
    'BenchmarkParameter',
    'CloudParameter',
    'ClusterParameter',
    'DistributionParameter',
    'GeoParameter',
    'InfluencerParameter',
    'LocalizationParameter',
    'PivotParameter',
    'SearchPublicationParameter',
    'SocialPerformanceParameter',
    'TopicParameter',
)


class Parameter(dict):
    """An object based on ``dict`` used to store the payload data sent with
    each request in RadarlyApi. Each road in the API used an object (which
    inherits from this class) to help you build the payload data which will
    be sent to the API. When the methods of Parameter object is used to build
    the object, some checks are computed on the values in order to assert that
    the payload data is correctly built.
    """
    pass


class AnalyticsParameter(Parameter,
                         StandardParameterMixin,
                         FctxMixin,
                         MetricsMixin,
                         FieldsMixin,
                         ClusterMixin):
    """Helper to build the payload sent when retrieving some statistics.
    This helper contains all the methods to restrict the set of publications
    (methods defined in radarly.parameters.field.StandardParameterMixin).

    Example:

        >>> from radarly.constants import INTERVAL, METRIC, PLATFORM
        >>> from radarly.constants import ANALYTICS_FIELD
        >>> start = datetime(2018, 1, 1)
        >>> end = datetime(2018, 1, 31)
        >>> param = AnalyticsParameter() \\
                .metrics(METRIC.DOC, METRIC.IMPRESSION, METRIC.ENGAGEMENT) \\
                .fields(ANALYTICS_FIELD.TONE, ANALYTICS.FOCUSES) \\
                .focuses(include=[1, 2, 3], exclude=[4, 5]) \\
                .fctx(1, 2, 3) \\
                .publication_date(start, end) \\
                .interval(INTERVAL.MONTH) \\
                .followers(1000, 5000) \\
                .media(MEDIA.IMAGE) \\
                .platforms(PLATFORM.INSTAGRAM) \\
                .query('danone')

    """
    pass


class BenchmarkParameter(Parameter,
                         RangeDateMixin,
                         TimezoneMixin,
                         IntervalMixin):
    """Helper to build the payload sent to the API when retrieving benchmark
    data.

    Example:

        >>> start = datetime(2018, 1, 1)
        >>> end = datetime(2018, 1, 31)
        >>> BenchmarkParameter() \\
                .timezone('Europe/Paris') \\
                .entities(1) \\
                .date_range(start, end)
    """
    def entities(self, *entities_ids):
        entities_ids = [str(entities_id) for entities_id in entities_ids]
        self['entities'] = ','.join(entities_ids)
        return self


class CloudParameter(Parameter,
                     StandardParameterMixin,
                     FctxMixin,
                     MetricsMixin,
                     TimezoneMixin,
                     FieldsMixin,
                     ClusterMixin):
    """Helper to build the payload sent to the API when retrieving cloud data.
    This helper contains all the methods to restrict the set of publications
    (methods defined in radarly.parameters.field.StandardParameterMixin).

    Example:

        >>> from radarly.constants import METRIC, PLATFORM
        >>> from radarly.constants import CLOUD_FIELD
        >>> start = datetime(2018, 1, 1)
        >>> end = datetime(2018, 1, 31)
        >>> cloud_param = CloudParameter() \\
                .focuses(include=[1, 2, 3, 4]) \\
                .fctx(*[1, 2, 3, 4]) \\
                .tones(TONE.POSITIVE) \\
                .timezone('Europe/Paris') \\
                .metrics(METRIC.DOC, METRIC.IMPRESSION, METRIC.REACH) \\
                .fields(CLOUD_FIELD.KEYWORDS, CLOUD_FIELD.MENTIONS) \\
                .publication_date(start, end)
    """
    pass


class ClusterParameter(Parameter,
                       StandardParameterMixin,
                       MetricsMixin,
                       SortMixin,
                       PaginationMixin):
    """Helper to build the payload sent to the API when retrieving clusters
    of publications. This helper contains all the methods to restrict the
    set of publications (methods defined in
    radarly.parameters.field.StandardParameterMixin).

    ..warning:: The value for the sort_by parameter are restricted.
        Check the ``AVAILABLE_SORT_BY`` class attribute to know the
        available parameters.
    """
    AVAILABLE_SORT_BY = [
        "volumetry",
        "radar.impression",
        "radar.reach"
    ]

    def __init__(self):
        super().__init__()
        self.flag(retweet=True)


class DistributionParameter(Parameter,
                            StandardParameterMixin,
                            IntervalMixin,
                            MetricsMixin,
                            GeoFilterMixin):
    """Helper to build the payload sent to the API when retrieving time
    distribution of some metrics. This helper contains all the methods
    to restrict the set of publications (methods defined in
    radarly.parameters.field.StandardParameterMixin).

    Example:

        >>> from radarly.constants import METRIC
        >>> start = datetime(2018, 1, 1)
        >>> end = datetime(2018, 1, 31)
        >>> param = DistributionParameter() \\
                .publication_date(start, end) \\
                .focuses(include=[1, 2, 3, 4], exclude=[5]) \\
                .flag(retweet=False) \\
                .metrics(METRIC.DOC, METRIC.IMPRESSION)
    """
    pass


class GeoParameter(Parameter,
                   StandardParameterMixin,
                   MetricsMixin,
                   FctxMixin,
                   GeoFilterMixin,
                   TimezoneMixin):
    """Helper to build the payload sent to the georgrid of the API.
    This helper contains all the methods to restrict the set of publications
    (methods defined in radarly.parameters.field.StandardParameterMixin).

    Example:

        >>> from radarly.constants import METRIC
        >>> start = datetime(2018, 1, 1)
        >>> end = datetime(2018, 1, 31)
        >>> geo_param = GeoParameter() \\
                .focuses(include=[1, 2, 3, 4]) \\
                .fctx(*[1, 2, 3, 4]) \\
                .flag(retweet=False) \\
                .geofilter() \\
                .metrics(METRIC.DOC) \\
                .publication_date(start, end)
    """
    pass


class InfluencerParameter(Parameter,
                          StandardParameterMixin,
                          SortMixin,
                          PaginationMixin):
    """Helper to build the payload when retrieving influencers' data.
    This helper contains all the methods to restrict the set of publications
    (methods defined in radarly.parameters.field.StandardParameterMixin).

    ..warning:: The value for the sort_by parameter are restricted.
        Check the ``AVAILABLE_SORT_BY`` class attribute to know the
        available parameters.

    Example:

        >>> from radarly.constants import PLATFORM
        >>> param = InfluencerParameter() \\
                .platforms(PLATFORM.FACEBOOK) \\
                .focuses(include=[1, 2, 3, 4]) \\
                .publication_date(start, end) \\
                .sort_by('reach') \\
                .pagination(0, 25)
    """
    AVAILABLE_SORT_BY = [
        # 'name',
        'impressions',
        'reach',
        'post'
    ]

    @classmethod
    def default(cls):
        param = cls()
        param = param.sort_by('name').sort_order('desc').pagination(0, 25)
        return param


class LocalizationParameter(Parameter,
                            StandardParameterMixin,
                            LocaleMixin,
                            GeoTypeMixin,
                            TimezoneMixin,
                            MetricsMixin):
    """Helper to build the payload sent to the API when retrieving distribution
    of publications by geographical zones. This helper contains all the methods
    to restrict the set of publications (methods defined in
    radarly.parameters.field.StandardParameterMixin).

    Example:

        >>> from radarly.constants import METRIC
        >>> param = LocalizationParameter() \\
                .locale('en_GB') \\
                .timezone('Europe/Paris') \\
                .metrics(METRIC.DOC)
    """
    pass


class PivotParameter(Parameter,
                     StandardParameterMixin,
                     TimezoneMixin,
                     MetricsMixin,
                     FctxMixin,
                     IntervalMixin):
    """Helper to build the payload for the pivot table road in the API.
    This helper contains all the methods to restrict the set of publications
    (methods defined in radarly.parameters.field.StandardParameterMixin).

    Example:

        >>> from radarly.constants import METRIC, INTERVAL
        >>> start = datetime(2018, 1, 1)
        >>> end = datetime(2018, 1, 31)
        >>> pivot_param = PivotParameter(pivot='Fragrances', against='focuses') \\
                .metrics(METRIC.DOC) \\
                .publication_date(start, end) \\
                .focuses(include=[1, 2, 3, 4]) \\
                .flag(retweet=False) \\
                .fctx(*[1, 2, 3, 4])

    """
    def __init__(self, pivot=None, against=None):
        super().__init__()
        if pivot: self['pivot'] = pivot
        if against: self['against'] = against

    def conf(self, pivot, against):
        self['pivot'] = pivot
        self['against'] = against
        return self


class SearchPublicationParameter(Parameter,
                                 StandardParameterMixin,
                                 SortMixin,
                                 PaginationMixin,
                                 FctxMixin,
                                 ClusterMixin,
                                 GeoFilterMixin):
    """Helper to build the payload sent to the API when you are searching
    pubications. This helper contains all the methods to restrict the set
    of publications (methods defined in
    radarly.parameters.field.StandardParameterMixin).

    ..warning:: The value for the sort_by parameter are restricted.
        Check the ``AVAILABLE_SORT_BY`` class attribute to know the
        available parameters.

    Example:

        >>> start = datetime(2018, 1, 1)
        >>> end = datetime(2018, 1, 31)
        >>> param = SearchPublicationParameter() \\
                .publication_date(start, end) \\
                .platforms(PLATFORM.INSTAGRAM) \\
                .languages('french', 'english', 'zh-cn', 'zh-tw') \\
                .flag(retweet=False, favorite=True) \\
                .tones(TONE.POSITIVE, TONE.NEUTRAL) \\
                .sort_by(BY.ENGAGEMENT) \\
                .pagination(start=0, limit=25)
    """
    AVAILABLE_SORT_BY = [
        'date',
        'radar.virality',
        'radar.engagement',
        'radar.reach',
        'radar.impression',
        'radar.rating',
        'random'
    ]

    @classmethod
    def default(cls):
        param = cls()
        param = param.sort_by('date').sort_order('desc').pagination(0, 25)
        return param


class SocialPerformanceParameter(Parameter,
                                 RangeDateMixin,
                                 TimezoneMixin):
    """Helper to build the payload sent to the API when retrieving
    social performance data.

    ..warning:: Only social accounts of some platforms can be analyzed. To
        check the available platforms, you can examine the
        ``AVAILABLE_PLATFORMs`` class attribute.

    Example:

        >>> from radarly.constants import PLATFORM
        >>> start = datetime(2018, 1, 1)
        >>> end = datetime(2018, 1, 31)
        >>> param = SocialPerformanceParameter() \\
                .timezone('Europe/Paris') \\
                .platform(PLATFORM.INSTAGRAM) \\
                .date_range(start, end)
    """
    AVAILABLE_PLATFORMS = [
        'instagram',
        'youtube',
        'twitter',
        'facebook',
        'linkedin',
        'sinaweibo'
    ]
    def platform(self, platform_value):
        """
        Args:
            platform_value (str): Platform of the social accounts on which the
                benchmark will be computed.
        """
        assert platform_value in self.AVAILABLE_PLATFORMS, \
            "The platform must be in {}".format(self.AVAILABLE_PLATFORMS)
        self['platform'] = platform_value
        return self

    def __call__(self):
        return urlencode(self)


class TopicParameter(Parameter,
                     StandardParameterMixin,
                     TimezoneMixin,
                     MetricsMixin,
                     LocaleMixin):
    """Helper to bulid the payload sent to the API when retrieving topic data.
    This helper contains all the methods to restrict the set of publications
    (methods defined in radarly.parameters.field.StandardParameterMixin).

    Example:

        >>> from radarly.constants import PLATFORM, METRIC
        >>> start = datetime(2018, 1, 1)
        >>> end = datetime(2018, 1, 31)
        >>> topic_param = TopicParameter() \\
                .locale('fr_FR') \\
                .metrics(METRIC.DOC, METRIC.IMPRESSION) \\
                .timezone('Europe/Paris') \\
                .focuses(include=[1, 2, 3, 4]) \\
                .publication_date(start, end) \\
                .platforms(PLATFORM.INSTAGRAM)
    """
    pass
