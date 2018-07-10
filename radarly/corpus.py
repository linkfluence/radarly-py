"""A corpus gathers several social accounts that can be monitored in Radarly.
"""

from .api import RadarlyApi
from .model import SourceModel


class Corpus(SourceModel):
    """Store information about a corpus.

    Args:
        created (datetime.datetime): creation date of the corpus
        id (int): unique identifier for the corpus
        name(str): name given to the corpus
        project_id (int): identifier of the project in which the corpus is
            registred.
        media_source (dict): dictionary which maps a platform with all the
            media sources available for this platform.
    """
    def __repr__(self):
        return '<Corpus.id={}.name={}>'.format(self['id'], self['name'])

    def __len__(self):
        """Get the number of media source registred in the corpus"""
        return sum([len(getattr(self, 'media_source')[platform])
                    for platform in getattr(self, 'media_source')])

    @classmethod
    def fetch_media(cls, project_id, corpora_id, api=None):
        """Retrieve all media sources linked to a corpus.

        Args:
            project_id (int): identifier of the project
            corpora_id (int): identifier of the corpus
            api (optional, RadarlyApi): API to use to perform the request.
                If ``None``, the default API will be used.
        """
        api = api or RadarlyApi.get_default_api()
        url = api.router.corpora['fetch_media'].format(
            project_id=project_id, corpora_id=corpora_id
        )
        return api.get(url)


class InfoCorpus(SourceModel):
    """Store small part of information about a corpus. In order to get the full
    object, you can use the ``expand`` method.

    Args:
        created (datetime.datetime): creation date of the corpus
        id (int): unique identifier for the corpus
        name(str): name given to the corpus
        project_id (int): identifier of the project in which the corpus is
            registred.
    """
    def __repr__(self):
        return '<InfoCorpus.id={}.name={}>'.format(self['id'], self['name'])

    @classmethod
    def _builder(cls, corpora):
        ans = []
        for corpus in corpora:
            del corpus['is_public']
            ans.append(cls(corpus))
        return ans

    def expand(self, api=None):
        """Get full data about a corpus (in particular to retrieve the media
        sources of the corpus.

        Args:
            api (optional, RadarlyApi): API object to use to perform the request. If
                ``None``, the default API will be used.
        Returns:
            Corpus: nearly the same object as ``InfoCorpus`` but with the
            ``media_source`` attribute in addition.
        """
        data_corpus = self.__dict__
        data_corpus['media_source'] = Corpus.fetch_media(self['project_id'],
                                                         self['id'],
                                                         api)
        return Corpus(data=data_corpus)
