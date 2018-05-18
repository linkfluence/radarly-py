"""
Metadata are all meta-information about a publication.
"""

from .model import SourceModel


class Metadata(SourceModel):
    """Dict-like object storing metadata of a publication

    Args:
        did (string): identifier for the publication
        trends:
        shared:
    """
    def __init__(self, data, document_id):
        super().__init__(data)
        self.did = document_id

    def __repr__(self):
        return '<Metadata.did={0.did}>'.format(self)
