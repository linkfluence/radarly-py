"""
The focuses in Radarly are used to store all the queries you defined
to capture publications.
"""

from .model import SourceModel
from .utils._internal import instance_builder


class Focus(SourceModel):
    """
    Dict-like object used to explore focus' data returned by the
    API.

    Args:
        id (int): unique identifier for the focus
        label (str): name of the focus (it corresponds to the name in
            Radarly)
        description (None or str): if available, describe the purpose of
            the focus
        created (datetime): creation date of the focus
        filter (dict): information about the query
    """
    def __init__(self, data):
        super().__init__(data)

    def __repr__(self):
        focus_id, label = getattr(self, 'id'), getattr(self, 'label')
        return '<Focus.id={}.label={}>'.format(focus_id, label)

    @classmethod
    def _builder(cls, focuses):
        return instance_builder(cls, focuses)
