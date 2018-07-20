"""
This module defines objects used to explore information about a Radarly User.
For security reasons, you can only retrieve information about the
current user of the API.
"""

from .api import RadarlyApi
from .model import SourceModel
from .project import InfoProject


class User(SourceModel):
    """Object used to explore user information returned by the API. Given that
    this object inherits from the ``SourceModel``, you can get the structure of the
    object with the ``draw_structure`` method.

    Examples:
        >>> user = User.find(uid='me')
        >>> user
        <User.id=1234.email='john.doe@linkfluence.com'>
        >>> user.keys()
        {'projects', 'current_project_id', ..., 'is_disabled'}

    Args:
        id (int): unique identifier of the user
        name (str): registred name of the user
        email (str): regitred email of the user
        projects (list[InfoProject]): list in which each item
            is an object storing some information about a project (notice
            that all information about a project are not stored in this
            object)
        created (datetime.datetime): creation datetime of the user
        ...
    """
    def __init__(self, data):
        super().__init__()
        translator = dict(
            projects=InfoProject._builder,
        )
        super().add_data(data, translator)

    def __repr__(self):
        uid, email = self['id'], self['email']
        return "<User.id={}.email='{}'>".format(uid, email)

    @classmethod
    def find(cls, uid, api=None):
        """
        Get information about an user.

        Args:
            uid (string): because you can only access data about you, this
                argument must be set to ``me``
            api (RadarlyApi, optional): API used to make the
                request. If None, the default API will be used.
        Returns:
            User: User object storing information retrieved from the API
        """
        api = api or RadarlyApi.get_default_api()
        if uid == 'me':
            user_data = api.get(api.router.user['me'])
            return cls(user_data)
        raise ValueError("The 'uid' argument must be set to 'me'.")
