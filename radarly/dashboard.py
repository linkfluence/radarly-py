"""
The Dashboard is an object in order to organize your project. It is a set
of focuses, social accounts and benchmark_entities.

In the Python client, a ``Dashboard`` object stored the ID of all the objects
contained in the dashboard.
"""

from .model import SourceModel
from .utils._internal import instance_builder


class Dashboard(SourceModel):
    """
    Object storing ID's of the focuses, social_accounts and benchmark entities
    which are grouped in the dashboard. The full objects are stored in the Project
    object.

    Args:
        id (int): unique identifier for the dashboard
        label (str): name of the dashboard (it correponds to the name in
            Radarly)
        description (None or str): if available, describes the purpose of
            the dashboard
        created (datetime): creation date of the dashboard
        focuses (list[int]): focuses' ids of the query in the dashboard
        social_accounts (list[dict]): list of all social accounts
            recorded in the dashboard. They are grouped by platforms.
        benchmark_entities (list[dict]): list of all benchmark entities
            in the dashboard.
        ...
    """
    def __init__(self, data):
        super().__init__()
        translator = dict(
            focuses=lambda focuses: [focus['id'] for focus in focuses],
        )
        super().add_data(data, translator)

    @classmethod
    def _builder(cls, dashboards):
        return instance_builder(cls, dashboards)

    def __repr__(self):
        dashboard_id, label = getattr(self, 'id'), getattr(self, 'label')
        return '<Dashboard.id={}.label={}>'.format(dashboard_id, label)
