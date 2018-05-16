"""
A tag is a label you can define in Radarly in order to sort publications.
"""

from .model import SourceModel


class Tag(SourceModel):
    """Dict-like object storing information about custom and user tags.

    Args:
        id (int): unique identifier of the tag
        type (str): *custom* or *user*
        label (str): name of the tags
        subtags (list[dict]): custom fields which can be created in Radarly
        ...
    """
    def __init__(self, data, tag_type):
        super().__init__()
        self.type = tag_type
        data['subtags'] = data.pop('values', [])
        super().add_data(data, None)

    def __repr__(self):
        label = getattr(self, 'label')
        return '<Tag.label={1}.type={0.type}>'.format(
            self, label
        )

    @classmethod
    def _builder(cls, tags):
        """Transform a dictionary of custom tags and user tags into a list of
        tags.

        Args:
            tags (dict): raw data about tags
        Returns:
            list[Tag]:
        """
        ans = [cls(custom_tag, 'custom') for custom_tag in tags['custom']]
        ans.extend([cls(custom_tag, 'user') for custom_tag in tags['user']])
        return ans
