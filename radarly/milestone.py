"""A milestone is a set of parameters used to add a label on a time period.
A milestone can then be used as a time's and timezone's filter."""

from .utils._internal import instance_builder
from .model import SourceModel


class Milestone(SourceModel):
    """This object stores all information about a milestone. Data store
    in the milestones can be used to configure the ``Parameter`` object.

    Args:
        id (str): unique identifier of the milestone
        name (str): name of the milestone
        description (str, optional): description of the milestone
        start_date (datetime.datetime): start date of the time period
            of the milestone.
        end_date (datetime.datetime): end date of the time period of
            the milestone
        interval (str): interval for the time period. Can be ``month``,
            ``week``, ``day`` or ``hour``.
        picture_id (str): ID of the custom picture for the milestone
        timezone (pytz.timezone): timezone of the milestone
        visibility (str): ``public`` or ``private``
    """
    @classmethod
    def _builder(cls, milestones):
        return instance_builder(cls, milestones)

    def __repr__(self):
        return '<Milestone.id={}.name={}>'.format(
            self['id'], self['name']
        )
