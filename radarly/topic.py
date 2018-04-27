"""
The topic wheel is a distribution of publications grouped by categories.
"""


class TopicWheel(list):
    """List-like object storing informations about the topics."""
    def __init__(self, data):
        super().__init__()
        self.extend(data)

    def __repr__(self):
        return '<Topics.length={}>'.format(len(self))


class Entities(list):
    """List-like object storing informations about entities"""
    def __init__(self, data):
        super().__init__()
        self.extend(data)

    def __repr__(self):
        return '<Entities.length={}>'.format(len(self))
