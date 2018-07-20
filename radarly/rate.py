"""
The API is submitted to several rates limits. The rates are returned in the
headers of each request. This modules defines the object used to parse the
request's headers and store this rates.
"""

import copy
import re

from .utils.router import Router


class RateConf:
    """Object storing information about the rate limit on each url of the
    ``Router`` object"""
    slow = [
        Router.influencer['search'],
        Router.distribution['fetch'],
        Router.analytics['global'],
        Router.cloud['fetch'],
        Router.localization['fetch'],
    ]
    medium = [
        Router.publication['search'],
        Router.publication['metadata'],
        Router.publication['raw'],
    ]

    @classmethod
    def get_category(cls, url):
        """Get the rate limit category of a URL.

        Args:
            url (string):
        Returns:
            string: category for this URL ('slow', 'medium' or 'default')
        """
        def into_pattern(path_url):
            """Transform a string with format option into a compiled regular
            expression"""
            if isinstance(path_url, str):
                format_pattern = r'{[a-zA-Z0-9_]*}'
                path_url = re.sub(format_pattern, '[a-zA-Z0-9]*', path_url)
                return re.compile(path_url)
            elif isinstance(path_url, (list, tuple)):
                return [into_pattern(url) for url in path_url]
            raise TypeError("'path_url' must be a string or a list")
        match_slow = any(
            [item.search(url) for item in into_pattern(cls.slow)]
        )
        match_medium = any(
            [item.search(url) for item in into_pattern(cls.medium)]
        )
        if match_slow:
            return 'slow'
        elif match_medium:
            return 'medium'
        return 'default'


class RateLimit:
    """Object which will count the remaining request"""
    def __init__(self):
        default = dict(limit=0, remaining=5000, reset=0)
        self.slow = copy.deepcopy(default)
        self.medium = copy.deepcopy(default)
        self.default = copy.deepcopy(default)

    def __repr__(self):
        log = []
        for category in ['slow', 'medium', 'default']:
            limit = getattr(self, category)
            percent = 100 * limit['limit'] / (limit['limit'] +  limit['remaining'])
            log.append((category, percent))
        log = '.'.join(['{}:{:.2f}%'.format(*item) for item in log])
        return '<RateLimit.{}>'.format(log)

    def update(self, url, data):
        """Parse a dictionnary which corresponds to the header of a response
        in order to get the current limit. The information retrieved is
        stored in the object.

        Args:
            url (string): url of the request
            data (dict): headers of the requests
        Returns:
            None:
        """
        right_limit = getattr(self, RateConf.get_category(url))
        right_limit['limit'] = int(data.get('X-Rate-Limit-Limit', right_limit['limit']))
        right_limit['remaining'] = int(
            data.get('X-Rate-Limit-Remaining', right_limit['remaining'])
        )
        right_limit['reset'] = int(data.get('X-Rate-Limit-Reset', right_limit['reset']))
        return None

    def is_reached(self, url):
        """Whether or not the current user can run some requests.

        Args:
            url (string): url which will be fectch by the pending request
        """
        right_limit = getattr(self, RateConf.get_category(url))
        return right_limit['remaining'] <= 0
