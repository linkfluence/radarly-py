"""
Social account registred in Radarly
"""

from .model import SourceModel


class SocialAccount(SourceModel):
    """Object storing information retrieved from the API about a social account
    registred in your project.

    .. warning:: This object does not have the same keys depending on the
        platform of the social account.

    Here are some useful keys (also available as instance's attributes):

    Args:
        id (str): unique identifier of the social account
        platform (str): platform of the social account
        url (str): link to your social account
        ...
    """
    def __init__(self, data, platform):
        super().__init__()
        self.platform = platform
        self.add_data(data)

    @classmethod
    def _builder(cls, social_accounts):
        social_objects = []
        for platform in social_accounts:
            social_objects.extend([
                cls(account, platform) for account in social_accounts[platform]
            ])
        return social_objects

    def __repr__(self):
        return '<SocialAccount.id={}.platform={}>'.format(
            self['id'], self['platform']
        )
