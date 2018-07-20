"""
Publications are all documents which match the query you have defined in
your projects.
"""


from os import getcwd
from os.path import abspath
from reprlib import repr as trunc_repr

import requests

from .api import RadarlyApi
from .constants import PLATFORM, TONE
from .exceptions import PublicationUpdateFailed
from .metadata import Metadata
from .model import GeneratorModel, SourceModel
from .utils.misc import parse_image_url
from .utils.jsonparser import snake_dict
from .utils.checker import check_geocode, check_language, check_list


class Publication(SourceModel):
    """Object base on ``SourceModel`` storing information about the
    publication. The structure of the model can be drawn with the
    ``draw_structure`` method.

    Args:
        uid (str): unique identifier of the publication
        origin (dict): dictionary which contains information about the
            platform where the publication comes from.
        permalink (str): link to the publication
        lang (str): lang of the publication
        date (datetime.datetime): creation date of the publication
        impression (int): number of impressions on the publication
        reach (int): estimated number of people reached by the publication
        tone (str): tone of the publication
        category (str): category of the publications
        user (dict): information about the author of the publication
    """
    def __init__(self, data, project_id):
        super().__init__()
        self.pid = project_id
        data = snake_dict(data, blacklist=[['radar', 'tag']])
        super().add_data(data)

    def __repr__(self):
        try:
            publication_uid = trunc_repr(self['uid'])
        except KeyError:
            publication_uid = None
        return '<Publication.uid={}>'.format(publication_uid)

    @classmethod
    def fetch(cls, project_id, parameter, api=None):
        """
        Get publications stored inside a project.

        Args:
            project_id (int): identifier of a project
            parameter (SearchPublicationParameter): parameters object
                made with the SearchPublicationParameter instance, which will
                be used as payload data in POST request. See
                ``SearchPublicationParameter`` to know how to build this
                object.
            api (RadarlyApi, optional): API object used to perform request. If
                None, it will use the default API.
        Returns:
            list[Publication]:
        """
        api = api or RadarlyApi.get_default_api()
        url = api.router.publication['search'].format(project_id=project_id)
        data = api.post(url, data=parameter)
        return [
            Publication(item, project_id) for item in data['hits']
        ]

    @classmethod
    def fetch_all(cls, project_id, parameter, api=None):
        """Get all publications matching given parameters. It yields
        publications.

        Args:
            project_id (int): identifier of your project
            parameter (SearchPublicationParameter): parameters object
                made with the SearchPublicationParameter instance, which will
                be used as payload data in POST request. See
                ``SearchPublicationParameter`` to know how to build this
                object.
            api (RadarlyApi, optional): API object used to perform request. If
                None, it will use the default API.
        Returns:
            PublicationsGenerator: list of publications. On each iterations, a
            Publication is yielded until there is no more publication.
        """
        api = api or RadarlyApi.get_default_api()
        return PublicationsGenerator(parameter,
                                     project_id=project_id, api=api)

    def get_metadata(self, params=None, api=None):
        """This method allows users to get document’s metadata.

        Args:
            params (dict, optional): parameter sent in the GET request. Default
                to None.
        Returns:
            Metadata: object storing metadata information
        """
        api = api or RadarlyApi.get_default_api()
        url = api.router.publication['metadata'].format(project_id=self.pid)
        params = {} if params is None else params
        params.update(dict(
            platform=self['origin']['platform'],
            uid=self['uid'],
        ))
        res_data = api.get(url, params=params)
        return Metadata(res_data, self['uid'])

    def get_raw(self, params=None, api=None):
        """Get the raw content of the publication.

        Args:
            params (dict, optional): parameter sent in the GET request. Default
                to None.
        Returns:
            dict: dictionary storing the raw content of the publication
        """
        api = api or RadarlyApi.get_default_api()
        doc_platform = self['origin']['platform']
        available_platform = [
            PLATFORM.FORUM,
            PLATFORM.BLOG,
        ]
        assert doc_platform in available_platform, \
            "{} is not compatible with raw content".format(doc_platform)
        url = api.router.publication['raw'].format(project_id=self.pid)
        params = {} if params is None else params
        params.update(dict(
            platform=doc_platform,
            uid=self['uid'],
        ))
        res_data = api.get(url, params=params)
        return res_data

    def set_tags(self, *args, **kwargs):
        """Update some information about a publication in Radarly. This
        method is based on the ``set_publication_tags`` function defined in
        the same module.

        .. warning:: Unlike the ``set_publication_tags``, this function returns
            None in case of success (the ``set_publication_tags`` returns a
            ``Publication`` object).

        Args:
            tone (str): tone of the publication. Can be `positive`,
                `negative`, `mixed` or `neutral`.
            language (str): alpha-2, alpha-3, or name of the language
            country (str): alpha-2, alpha-3 or name of the country
            keywords (list[str]): list of keywords for the publication
            custom_tags (dict[str -> list[str]]): value of the custom tags
                to set. The template for this argument is::

                {<label of the custom_tag>: [<label of the subtag>]}.

                Example: Given two tags (the first one named ``Product``
                with ``Shoes``, ``T-Shirt`` and ``Clothes`` as subtags and
                the second one named ``Price`` with ``High``, ``Medium``
                and ``Low`` as subtags), a valid value for the ``custom_tags``
                could be::

                    {'Product': ['Clothes', 'T-Shirt'], 'Price': ['High']}
        Raises:
            PublicationUpdateFailed: error raised if the publication failed
        Returns:
            None
        """

        publication = set_publication_tags(
            *args,
            project_id=getattr(self, 'pid'),
            uid=getattr(self, 'uid'),
            platform=getattr(self, 'origin')['platform'],
            **kwargs
        )
        self.add_data(publication.__dict__)
        return None


    def download(self, output_dir=None, chunk_size=1024):
        """Download the publication if it is an image or video.

        .. warning:: This function will not raised an error even if the
            download fails. To know if all the download succeed, compare the
            media object of a publication with the response of the function.

        Args:
            output_dir (str, optional): folder where the downloaded images must
                be saved. The folder must already exists. Default to the
                current working directory.
            chunk_size (int, optional): chunk size used during the file
                download with ``requests``. Default to 1024.
        Returns:
            dict[str]: filepath of the downloaded medias. This dictionary has
            quite the same structure of the ``media`` attribute of the
            publication.
        """
        def download_content(content_link, output_dir):
            """Download the content of a media and save it in a existing
            directory.

            Args:
                content_link (str):
                output_dir (str):
            Returns:
                dict: local version of the media object
            """
            if content_link is None: return None
            res = requests.get(content_link, stream=True)
            try:
                res.raise_for_status()
            except requests.exceptions.HTTPError:
                return None
            img_name, img_format = parse_image_url(res.url)
            filepath = '{}/{}.{}'.format(output_dir, img_name, img_format)

            with open(filepath, mode='wb') as image_file:
                for chunk in res.iter_content(chunk_size=chunk_size):
                    image_file.write(chunk)

            return abspath(filepath)

        output_dir = output_dir or getcwd()

        media_links = dict(
            image=[],
            video=[]
        )
        if self['media'] and self['media']['image']:
            downloaded_images = [
                download_content(item, output_dir) for item in self['media']['image']
            ]
            media_links['image'].extend(list(filter(None, downloaded_images)))
        if self['media'] and self['media']['video']:
            downloaded_videos = [
                {
                    'url': download_content(item['url'], output_dir),
                    'thumbnail': download_content(item['thumbnail'], output_dir)
                } for item in self['media']['video']
            ]
            media_links['video'].extend(
                filter(lambda x: x['url'] and x['thumbnail'], downloaded_videos)
            )

        return media_links


class PublicationsGenerator(GeneratorModel):
    """Generator which yields all publications matching some payload.

    Args:
        search_param (SearchPublicationParameter):
        project_id (int): identifier of the project
        api (RadarlyApi): api to use to perform requests
    Yields:
        Publication:
    """
    def _fetch_items(self):
        """Get next range of publications"""
        url = self._api.router.publication['search'].format(
            project_id=self.project_id
        )
        res_data = self._api.post(url, data=self.search_param)
        self.total = res_data['total']
        self._items = (
            Publication(item, self.project_id)
            for item in res_data['hits']
        )
        div = self.total // self.search_param['limit']
        reste = self.total % self.search_param['limit']
        self.total_page = div
        if reste != 0: self.total_page += 1
        self.search_param = self.search_param.next_page()

    def __repr__(self):
        return '<PublicationsGenerator.total={}.total_page={}>'.format(
            self.total, self.total_page
        )


def set_publication_tags(project_id, uid, platform,
                         tone=None, language=None, country=None,
                         keyword=None, custom_tags=None, api=None):
    """Update some fields in a publication in Radarly. Only specific field
    can be updated. This function is outside the ``Publication`` class in order
    to give you the opportunity to update a publication without having the full
    object. The ``set_tags`` method of ``Publication`` uses this function so
    there is no big differences between theses two functions.

    Args:
        tone (str): tone of the publication. Can be `positive`,
            `negative`, `mixed` or `neutral`.
        language (str): alpha-2, alpha-3, or name of the language
        country (str): alpha-2, alpha-3 or name of the country
        keywords (list[str]): list of keywords for the publication
        custom_tags (dict[str -> list[str]]): value of the custom tags
            to set. The tags must already exist. The template for this
            argument is::

            {<label of the custom_tag>: [<label of the subtag>]}.

            Example: Given two tags (the first one named ``Product``
            with ``Shoes``, ``T-Shirt`` and ``Clothes`` as subtags and
            the second one named ``Price`` with ``High``, ``Medium``
            and ``Low`` as subtags), a valid value for the ``custom_tags``
            could be::

                {'Product': ['Clothes', 'T-Shirt'], 'Price': ['High']}
    Raises:
        PublicationUpdateFailed: error raised if the publication failed
    Returns:
        Publication: publication which was updated
    """

    def check_update(pub, tone, language, country,
                     keyword, custom_tags):
        """Check the publication's update."""
        not_updated_fields = []
        if tone and pub['tone'] != tone:
            not_updated_fields.append('tone')
        if keyword and pub['keyword'] != keyword:
            not_updated_fields.append('keyword')
        if language and pub['lang'] != language:
            not_updated_fields.append('lang')
        if country and pub['geo']['inferred']['country'] != country:
            not_updated_fields.append('geo.inferred.country')
        if custom_tags:
            _ = [
                not_updated_fields.append('radar.tag.custom.{}'.format(key))
                for key in custom_tags
                if pub['radar']['tag']['custom'][key] != custom_tags[key]
            ]
        if not_updated_fields:
            raise PublicationUpdateFailed(fields=not_updated_fields)
        return None

    payload = {}
    if tone:
        _ = TONE.check(tone)
        payload['tone'] = tone
    if language:
        language = check_language(language)[0].lower()
        payload['lang'] = language
    if keyword is not None:
        check_list(keyword, str, "`keyword` must be a list of string.")
        payload['keyword'] = {'set': keyword}
    if country:
        payload['country'] = check_geocode(country)
    if custom_tags:
        _ = {
            key: check_list(custom_tags[key], str,
                            ("The value for the field `{}` must be a "
                             "list of `{}` element").format(key, str(str)))
            for key in custom_tags
        }
        custom_tags_setter = {
            label: {'set': custom_tags[label]} for label in custom_tags
        }
        payload['radar'] = {'tag': {'custom': custom_tags_setter}}

    params = dict(
        uid=uid,
        platform=platform,
    )
    payload = {
        "doc": payload
    }
    api = api or RadarlyApi.get_default_api()
    url = api.router.publication['set_tag'].format(
        project_id=project_id
    )
    publication = api.post(url, params=params, data=payload)
    publication = Publication(data=publication, project_id=project_id)

    check_update(publication, tone, language, country,
                 keyword, custom_tags)

    return publication
