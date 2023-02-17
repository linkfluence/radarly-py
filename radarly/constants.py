"""
The Radarly API uses several constants especially in the search parameters.
In order to avoid you bad requests to the API, we have defined
several objects which represents all the constants which can be used to
parametrize the requests. These constants are used in ``radarly.parameters``
in order to check if the given parameters you enter are correct.
"""

from .utils.misc import load_data, dict_to_namedtuple, flat


__all__ = [
    'ANALYTICS_FIELD',
    'BY',
    'CATEGORY',
    'CLOUD_FIELD',
    'GENDER',
    'GEOTYPE',
    'INTERVAL',
    'MEDIA',
    'METRIC',
    'ORDER',
    'PLATFORM',
    'TONE',
    'EMOTION'
]


def _set_categories_data(cls):
    """Dynamically load the categories data in ``CATEGORY`` class

    Args:
        class in which the data must be injected
    Returns:
        None:
    """
    categories = load_data('assets/categories.json')
    for category_name in categories:
        dict_category = {
            item.replace('-', '_').upper(): '.'.join([category_name, item])
            for item in categories[category_name]
        }
        namedtuple = dict_to_namedtuple(category_name, dict_category)
        setattr(cls, category_name.upper(), namedtuple)
    return None


class CheckerMixin:
    """Mixin in order to check if the parameters are correct"""
    @classmethod
    def check(cls, elements):
        """Check that the given values for a specific key in payload data are
        right.

        Args:
            elements (list or string): if ``elements`` is a string, check if it
                is an available option for the key. If ``elements`` is a list
                or tuple, call the function on all item in the list.
        Raises:
            AssertionError: raised if one element isn't right.
        Returns:
            boolean: True if all is ok
        """
        if isinstance(elements, (list, tuple)):
            return all([cls.check(element) for element in elements])
        attributes = dict(cls.__dict__)
        for key in attributes.copy():
            if ((key.startswith('__') and key.endswith('__'))
                    or callable(attributes[key])
                    or isinstance(attributes[key], classmethod)):
                _ = attributes.pop(key)
        assert elements in attributes.values(), \
            "{} is an unknown option for the '{}' parameter".format(
                elements, cls.__name__
            )
        return True


class PLATFORM(CheckerMixin):
    """List of origin platforms for the publications in Radarly"""
    BLOG = 'blog'
    COMMENT = 'comment'
    DAILYMOTION = 'dailymotion'
    FACEBOOK = 'facebook'
    FORUM = 'forum'
    GPLUS = 'gplus'
    INSTAGRAM = 'instagram'
    LINKEDIN = 'linkedin'
    MEDIA = 'media'
    REVIEW = 'review'
    SINAWEIBO = 'sinaweibo'
    TWITTER = 'twitter'
    VKONTAKTE = 'vkontakte'
    WEBSITE = 'website'
    WECHAT = 'wechat'
    YOUKU = 'youku'
    YOUTUBE = 'youtube'
    TIKTOK = 'tiktok'
    LITTLEREDBOOK = 'littleredbook'
    PINTEREST = 'pinterest'


class TONE(CheckerMixin):
    """Tone of a publication given by our algorithms"""
    MIXED = 'mixed'
    NEGATIVE = 'negative'
    NEUTRAL = 'neutral'
    POSITIVE = 'positive'


class EMOTION(CheckerMixin):
    """Emotion of a publication given by our algorithms"""
    JOY = 'joy'
    LOVE = 'love'
    SURPRISE = 'surprise'
    FEAR = 'fear'
    ANGER = 'anger'
    DISGUST = 'disgust'
    FEAR = 'sadness'

class MEDIA(CheckerMixin):
    """Media's type of publications"""
    IMAGE = 'image'
    VIDEO = 'video'


class GEOTYPE(CheckerMixin):
    """Geographic area's type used for geographical distribution"""
    COUNTRY = 'country'
    TOWN = 'town'


class CATEGORY(CheckerMixin):
    """Categories defined by our algorithm which sorts posts by topics.

    .. note:: This class is initialized dynamically.
    """
    @classmethod
    def check(cls, elements):
        if isinstance(elements, (list, tuple)):
            return all([cls.check(element) for element in elements])
        attributes = dict(cls.__dict__)
        for key in attributes.copy():
            if ((key.startswith('__') and key.endswith('__'))
                    or callable(attributes[key])
                    or isinstance(attributes[key], classmethod)):
                _ = attributes.pop(key)
        attributes = flat([list(attributes[item]) for item in attributes])
        assert elements in attributes, \
            "{} is an unknown option for the '{}' parameter".format(
                elements, cls.__name__
            )
        return True

_set_categories_data(CATEGORY)


class GENDER(CheckerMixin):
    """Gender of people on the publication if available."""
    FEMALE = 'F'
    MALE = 'M'


class CLOUD_FIELD(CheckerMixin): # pylint: disable=C0103
    """Cloud fields which are available as parameters."""
    AFFECTS = 'affects'
    EMOJIS = 'emojis'
    HASHTAGS = 'hashtags'
    KEYWORDS = 'keywords'
    MENTIONS = 'mentions'
    NAMED_ENTITIES = 'namedEntities'


class ANALYTICS_FIELD: # pylint: disable=C0103
    """Kind of analytics you want to retrieve when you ask statistics
    about a query or set of queries."""
    CATEGORIES = 'categories'
    COUNTRIES = 'countries'
    DEMOGRAPHY = 'demography'
    DENSITY_PERSON = 'persons'
    FOCUSES = 'focuses'
    GENDERS = 'genders'
    IMAGE_GENDERS = 'imageGenders'
    LANGUAGES = 'languages'
    LOGOS = 'logos'
    OCCUPATIONS = 'occupations'
    OPERATING_SYSTEMS = 'operatingSystems'
    PLATFORMS = 'platforms'
    TONES = 'tones'
    EMOTIONS = 'emotions'


class METRIC(CheckerMixin):
    """Metrics on the application. Notice that other metrics then DOC need
    some computations so it can be slower."""
    DOC = 'doc'
    IMPRESSION = 'impression'
    REACH = 'reach'
    REPOST = 'repost'
    ENGAGEMENT = 'engagement'

class ORDER(CheckerMixin):
    """Parameter used in order to choose the sort order in a list returned
    by the API. This parameter shoud ideally be used with the sortBy parameter.
    """
    ASCENDANT = 'asc'
    DESCENDANT = 'desc'

class BY(CheckerMixin):
    """Parameter used to sort the results returned by the API"""
    DATE = 'date'
    ENGAGEMENT = 'radar.engagement'
    IMPRESSION = 'radar.impression'
    INFLUENCER_IMPRESSION = 'impressions'
    INFLUENCER_POST = 'post'
    INFLUENCER_REACH = 'reach'
    RANDOM = 'random'
    RATING = 'radar.rating'
    REACH = 'radar.reach'
    VIRALITY = 'radar.virality'
    VOLUMETRY = 'volumetry'

class INTERVAL(CheckerMixin):
    """Interval to use in order to group results when a temporal distribution
    is returned by the API."""
    DAY = 'day'
    HOUR = 'hour'
    MONTH = 'month'
    YEAR = 'year'
