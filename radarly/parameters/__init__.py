"""
Parameters object sent as payload data.
"""

import json
from urllib.parse import urlencode

from .field import (ClusterMixin, FctxMixin, FieldsMixin, GeoFilterMixin,
                    IntervalMixin, LocaleMixin, MetricsMixin, PaginationMixin,
                    RangeDateMixin, SortMixin, StandardParameterMixin,
                    TimezoneMixin)


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
    """A dict-like object used to store the payload data sent with each
    request in RadarlyApi. Each road in the API used an object (which inherits
    from this class) to build the payload data which will be sent to the API.
    When the methods of Parameter object is used to build the object, some
    checks are computed on the values in order to assert that the payload data
    are correctly made.
    """
    pass


class AnalyticsParameter(Parameter,
                         StandardParameterMixin,
                         FctxMixin,
                         MetricsMixin,
                         FieldsMixin,
                         ClusterMixin):
    """Parameters used when retrieving some statistics.

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
    """Parameters used as payload when retrieving benchmark datas.

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
                     MetricsMixin,
                     TimezoneMixin,
                     FieldsMixin,
                     ClusterMixin):
    """Parameters used when retrieving cloud datas.

    Example:

        >>> from radarly.constants import METRIC, PLATFORM
        >>> from radarly.constants import CLOUD_FIELD
        >>> start = datetime(2018, 1, 1)
        >>> end = datetime(2018, 1, 31)
        >>> cloud_param = CloudParameter() \\
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
    """Parameters used as payload when retrieving clusters of publications"""
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
                            MetricsMixin):
    """Parameters used when retrieving a time distribution of some metrics.

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
    """Parameters used as payload when retrieving geographical distribution
    datas

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
    """Parameter used when retrieving influencers' data.

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
                            TimezoneMixin,
                            MetricsMixin):
    """Parameters used when retrieving a geo distribution.

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
    """Parameters used to build pivot table.

    Example:

        >>> from radarly.constants import METRIC, INTERVAL
        >>> start = datetime(2018, 1, 1)
        >>> end = datetime(2018, 1, 31)
        >>> pivot_param = PivotParameter(pivot='Fragrances', against='focuses') \\
                .publication_date(start, end) \\
                .focuses(include=[1, 2, 3, 4]) \\
                .fctx(*[1, 2, 3, 4]) \\
                .metrics(METRIC.DOC) \\
                .interval(INTERVAL.DAY) \\
                .flag(retweet=False)

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
                                 ClusterMixin):
    """Parameters used when retrieving some publications.

    Example:

        >>> start = datetime(2018, 1, 1)
        >>> end = datetime(2018, 1, 31)
        >>> param = SearchPublicationParameter() \\
                .publication_date(start, end) \\
                .platforms(PLATFORM.INSTAGRAM) \\
                .pagination(0, 10)
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
    """Parameters used when retrieving social performance data

    Example:

        >>> from radarly.constants import PLATFORM
        >>> start = datetime(2018, 1, 1)
        >>> end = datetime(2018, 1, 31)
        >>> param = SocialPerformanceParameter() \\
                .timezone('Europe/Paris') \\
                .platform(PLATFORM.INSTAGRAM) \\
                .date_range(start, end)
    """
    def platform(self, platform_value):
        right_platforms = [
            'instagram',
            'youtube',
            'twitter',
            'facebook',
            'linkedin',
            'sinaweibo'
        ]
        assert platform_value in right_platforms, \
            "The platform must be in {}".format(right_platforms)
        self['platform'] = platform_value
        return self

    def __call__(self):
        return urlencode(self)


class TopicParameter(Parameter,
                     StandardParameterMixin,
                     TimezoneMixin,
                     MetricsMixin,
                     LocaleMixin):
    """Parameters used as payload when retrieving topic datas.

    Example:

        >>> from radarly.constants import PLATFORM, METRIC
        >>> start = datetime(2018, 1, 1)
        >>> end = datetime(2018, 1, 31)
        >>> topic_param = TopicParameter() \\
                .locale('fr_FR') \\
                .metrics(METRIC.DOC, METRIC.IMPRESSION) \\
                .timezone('Europe/Paris') \\
                .focuses(include=[1, 2, 3, 4]) \\
                .publication_date(start, end)
    """
    pass
