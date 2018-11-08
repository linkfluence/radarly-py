"""A field in parameter is a (key , value) pair in the dictionary sent as
payload to the API. For most fields, the value is checked in
order to be sure that the parameter is built properly. This way, bad
requests can be avoided."""

import pytz

from ..constants import (CATEGORY, GENDER, GEOTYPE, INTERVAL, MEDIA, METRIC,
                         ORDER, PLATFORM, TONE)
from ..utils.checker import (check_date, check_geocode, check_language,
                             check_list)


class AuthorMixin:
    """Field used to build all the author related parameters in the payload
    data"""
    def author_birth_date(self, start=None, end=None):
        """Restrict the publications to the right interval for author's
        birthdate.

        Args:
            start (datetime.datetime): Min birthdate of the author
            end (datetime.datetime): Max birthdate of the author
        """
        start = check_date(start)
        end = check_date(end)
        if start or end:
            self['birthDate'] = dict()
            if start: self['birthDate'].update(gt=start)
            if end: self['birthDate'].update(lt=end)
        return self

    def author_has_children(self, has_children):
        """Restricts to author that declares to have children.

        Args:
            has_children (bool): whether or note the author has children
        """
        assert isinstance(has_children, bool), \
            "'has_children' must be a boolean"
        self.update(hasChildren=has_children)
        return self

    def author_in_relationship(self, in_relationship):
        """Restricts to author that declares to be in a relationship

        Args:
            in_relationship (bool): whether or not the author must be in a
                relationship"""
        assert isinstance(in_relationship, bool), \
            "'in_relationship' must be a boolean"
        self.update(inRelationship=in_relationship)
        return self

    def author_verified(self, verified):
        """Restricts to author with certified accounts.

        Args:
            verified (bool): whether or not the author has a certified
                account
        """
        assert isinstance(verified, bool), 'verified must be a boolean'
        self.update(verified=verified)
        return self

    def author_id(self, *author):
        """Restric the set of publications to those which are created by
        specific authors.

        Args:
            *author (list[Dict[str, str]]): each author object is an object
                which support the __getitem__ method and must have both
                'id' and 'platform' keys.
        """
        author_ids = [
            '(user.{platform}.id:{uid})'.format(
                platform=author_id['platform'], uid=author_id['id']
            ) for author_id in author
        ]
        author_ids = ' OR '.join(author_ids)
        query = self.get('query', '')
        self['query'] = '{} AND ({})'.format(query, author_ids) if query \
            else '({})'.format(author_ids)
        return self


class CategoryMixin:
    """Field used to build the *category* parameter in the payload data"""
    def categories(self, *category_name):
        """List of the Radarly categories you want to restrict your search.

        Args:
            *category_name (str): list of categories. You can use the CATEGORY
                object of ``radarly.constants`` module to know the available
                category."""
        CATEGORY.check(category_name)
        if category_name: self.update(categories=list(category_name))
        return self


class ClusterMixin:
    def clusters(self, *cluster_ids):
        check_list(cluster_ids, str)
        self['stories'] = cluster_ids
        return self


class CorporaMixin:
    """Field used to build the *corpora* parameter in the payload data"""
    def corpora(self, *corpora_ids):
        """List of the Radarly registred corpora ids you want to search into"""
        check_list(corpora_ids, str)
        if corpora_ids: self.update(corpora=list(corpora_ids))
        return self


class DateMixin:
    """Field used to build all date related parameters in the payload data"""
    def creation_date(self, created_before=None, created_after=None):
        """Restricts using indexation date"""
        created_before = check_date(created_before)
        created_after = check_date(created_after)
        if created_before or created_after:
            self['date'] = dict()
            if created_before: self['date']['createdBefore'] = created_before
            if created_after: self['date'].update(createdAfter=created_after)
        return self

    def publication_date(self, start=None, end=None):
        """Restricts using publication date"""
        start = check_date(start)
        end = check_date(end)
        if start or end:
            if start: self.update({'from': start})
            if end: self.update(to=end)
        return self


class EmojiMixin:
    """Field used to build the *emojis* parameter in the payload data"""
    def emoji(self, charts=None, annotations=None):
        """Args:
            charts (list):
            annotations (list):
        """
        if charts or annotations:
            self['emoji'] = dict()
            if charts: self['emoji'].update(charts=charts)
            if annotations: self['emoji'].update(annotations=annotations)
        return self


class FctxMixin:
    """Field used to build the *fctx* parameter in the payload data"""
    def fctx(self, *fctx_list):
        self['fctx'] = list(fctx_list)
        return self


class FieldsMixin:
    """Field used to build the *fields* parameter in the payload data"""
    def fields(self, *fields_list):
        self['fields'] = list(fields_list)
        return self


class FlagMixin:
    """Field used to build the *flag* parameter in the payload data"""
    def flag(self, favorite=None, trash=None, retweet=None):
        """Enables the retrieving of favorites or non-favorites, of trashed
        publications or of retweets."""
        args = [f for f in [favorite, trash, retweet] if f]
        check_list(args, bool)
        self['flag'] = dict()
        self['flag'].update(favorite=favorite, trash=trash, rt=retweet)
        return self


class FocusMixin:
    """Field used to build the *focuses* parameter in the payload data"""
    def focuses(self, include=None, exclude=None):
        """List of the Radarly registred query ids you want to search into.

        Args:
            include (list): query ids to include
            exclude (list): query ids to exclude.
        """
        if include or exclude:
            self['focuses'] = []
        if include:
            check_list(include, int)
            self['focuses'].extend(
                [dict(id=query, include=True) for query in include]
            )
        if exclude:
            check_list(exclude, int)
            self['focuses'].extend(
                [dict(id=query, include=False) for query in exclude]
            )
        return self


class FollowerMixin:
    """Field used to build the *followers* parameter in the payload data"""
    def followers(self, minf=None, maxf=None):
        """Restricts to the min/max number of followers of a
        twitter/instagram/sinaweibo source."""
        if minf or maxf:
            self['followers'] = dict()
            if minf:
                assert isinstance(minf, int),  \
                    'Min values of followers must be an integer'
                self['followers'].update(gt=minf)
            if maxf:
                assert isinstance(maxf, int), \
                    'Max values of followers must be  an integer'
                self['followers'].update(lt=maxf)
        return self


class GenderMixin:
    """Field used to build the *genders* parameter in the payload data"""
    def genders(self, *gender_list):
        """Restricts to the given genders.

        Args:
            *gender_list (string): list of wanted gender.
        """
        GENDER.check(gender_list)
        self.update(genders=list(gender_list))
        return self


class GeoFilterMixin:
    def geofilter(self, polygon=None):
        self['geoFilter'] = dict()
        if polygon is None:
            polygon = [
                {"lon": -180, "lat": 81.01649},
                {"lon": 180, "lat": 81.01649},
                {"lon": 180, "lat": -58.94237},
                {"lon": -180, "lat": -58.94237},
                {"lon": -180, "lat": 81.01649}
            ]
        self['geoFilter']['filterPolygon'] = polygon
        return self


class GeoMixin:
    """Field used to build the *geo* parameter in the payload data"""
    def geo(self, gtype, glist):
        """List of items following geo.type (fr, gb,...); Restricts to the
        given countries, given by an ISO 3166-1 alpha-2

        Args:
            gtype (str): the type of geographical place (country or town)
            glist (list[str]): if ``gtype`` is country, you can pass a
                country name, its alpha-2 code, its alpha-3 or its official
                name.
        """
        GEOTYPE.check(gtype)
        if gtype == GEOTYPE.COUNTRY:
            glist = check_geocode(glist)
        self['geo'] = dict(type=gtype, list=glist)
        return self


class GeoTypeMixin:
    """Field used to specify the region type for geographical distribution"""
    def geo_type(self, gtype):
        """
        Args:
            gtype (str):
        """
        assert gtype in ['region', 'town'], \
            "gtype is an unknown option for the geographical type"
        self['geo_type'] = gtype
        return self


class IntervalMixin:
    """Field used to build the *interval* parameter in the payload data"""
    def interval(self, interval_value):
        INTERVAL.check(interval_value)
        self['interval'] = interval_value
        return self


class KeywordMixin:
    """Field used to build all keywords related parameter in the payload data"""
    def _builder_kw(self, name, *args):
        check_list(args, str)
        self.setdefault('keywords', {})
        self['keywords'][name] = list(args)
        return self

    def hashtags(self, *hashtags):
        """Restrics to the given hashtags.

        Args:
            *hashtags (list[str]):
        """
        return self._builder_kw('hashtags', *hashtags)

    def mentions(self, *mentions):
        """Restrics to the given @mentions

        Args:
            *mentions (list[str]):
        """
        return self._builder_kw('mentions', *mentions)

    def named_entities(self, *named_entities):
        """Restrics to the given named entities.

        Args:
            *named_entities (list[str]):
        """
        return self._builder_kw('namedEntities', *named_entities)

    def keywords(self, *keywords):
        """Restrics to the given keywords (manual or trigger tags).

        Args:
            *keywords (list[str]):
        """
        return self._builder_kw('keywords', *keywords)


class LanguageMixin:
    """Field used to build the *langauages* parameters in the payload data."""
    def languages(self, *language_list):
        """Restricts to the given languages, given by an ISO 639-1 code.

        Args:
            *language_list (string): list of all wanted languages. You can
                pass a language name, its alpha-2 code or its alpha-3 code.
        """
        language_list = check_language(language_list)
        self.update(languages=list(language_list))
        return self


class LocaleMixin:
    """Field used to build the *locale* parameter in the payload data"""
    def locale(self, locale_value):
        self['locale'] = locale_value
        return self


class MediaMixin:
    """Field used to build the *media* parameter in the payload data"""
    def media(self, *media_list):
        """Restricts to the given media types.

        Args:
            *media_list (string):
        """
        MEDIA.check(media_list)
        self['media'] = list(media_list)
        return self


class MetricsMixin:
    """Field used to build the *metrics* parameter in the payload data"""
    def metrics(self, *metrics_val):
        METRIC.check(metrics_val)
        self['metrics'] = list(metrics_val)
        return self


class PaginationMixin:
    """Field used to build all pagination related parameters in the payload
    data
    """
    def pagination(self, start=0, limit=25):
        assert isinstance(start, int), 'start index must be  an integer'
        assert isinstance(limit, int), 'limit must be  an integer'
        assert (start >= 0) and (limit > 0), 'Weird'
        self.update(start=start, limit=limit)
        return self

    def next_page(self):
        limit = self.get('limit', 25)
        start = self.get('start', -limit) + limit
        self.update(start=start, limit=limit)
        return self


class PlatformMixin:
    """Field used to build the *platforms* parameter in the payload data.
    You can check the available options in radarly.constants module."""
    def platforms(self, *platform_list):
        """Source platforms for publications in Radarly. The available
        platforms are available in the `platforms` object in the `constants`
        module of `radarly`.

        Args:
            *platform_list (string): list of all wanted platforms
        """
        PLATFORM.check(platform_list)
        self.update(platforms=list(platform_list))
        return self


class QueryMixin:
    """Field used to build the *query* parameter in the payload data"""
    def query(self, query):
        """A UTF-8 search query string of maximum 4K characters maximum,
        including operators. eg: “linkfluence AND radarly”. For additional
        information on how to build the query, you can check the official
        documentation.

        Args:
            query (string):
        """
        assert isinstance(query, str), 'Query shoud be a string.'
        self.update(query=query)
        return self


class RangeDateMixin:
    """Field used to build the range date parameter."""
    def date_range(self, start=None, end=None):
        start = check_date(start)
        end = check_date(end)
        if start or end:
            if start: self['from'] = start
            if end: self['to'] = end
        return self


class SortMixin:
    """Field used to build the sort related parameter in the payload data"""
    def sort_by(self, sort_by_filter):
        assert sort_by_filter in self.AVAILABLE_SORT_BY, \
            'Unknown sortBy parameter'
        self.update(sortBy=sort_by_filter)
        return self

    def sort_order(self, sort_order_filter):
        ORDER.check(sort_order_filter.lower())
        self.update(sortOrder=sort_order_filter)
        return self


class TagMixin:
    """Field used to build the *tags* parameter in the payload data"""
    def tags(self, user_tags=None, custom_fields=None):
        """List of Radarly registred influencers group tags or custom Fields
        values under format you want to restrict to."""
        if custom_fields:
            self.setdefault('tags', dict())
            self['tags']['customFields'] = custom_fields
        if user_tags:
            self.setdefault('tags', dict())
            self['tags']['userTags'] = user_tags
        return self


class TimezoneMixin:
    """Field used to build the *timezone* parameter in the payload data"""
    def timezone(self, time_zone):
        if time_zone not in pytz.all_timezones:
            raise ValueError('The timezone has not been recognized.')
        self['tz'] = time_zone
        return self


class ToneMixin:
    """Field used to build the *tones* parameter in the payload data"""
    def tones(self, *tone_list):
        """Restricts to the given tones. All available tones are given in
        the `tones` object of the `constants` module.

        Args:
            *tone_list (string):
        """
        TONE.check(tone_list)
        self.update(tones=list(tone_list))
        return self

class EmotionMixin:
    """Field used to build the *emotions* parameter in the payload data"""
    def emotions(self, *emotion_list):
        """Restricts to the given emotions. All available emotions are given in
        the `emotions` object of the `constants` module.

        Args:
            *emotion_list (string):
        """
        TONE.check(emotion_list)
        self.update(emotions=list(emotion_list))
        return self


class StandardParameterMixin(QueryMixin,
                             PlatformMixin,
                             LanguageMixin,
                             GenderMixin,
                             AuthorMixin,
                             ToneMixin,
                             MediaMixin,
                             KeywordMixin,
                             EmojiMixin,
                             FollowerMixin,
                             FlagMixin,
                             DateMixin,
                             GeoMixin,
                             FocusMixin,
                             CorporaMixin,
                             CategoryMixin,
                             TagMixin,
                             IntervalMixin):
    """Parameter which can be used in most of requests"""
    pass
