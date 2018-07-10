"""
Used to control Python object type
"""

import pycountry
from dateutil.parser import parse

from .misc import flat


def check_date(date_object):
    """Convert a date into the right for API"""
    if date_object is None: return None
    if isinstance(date_object, str):
        date_object = parse(date_object)
    date_object = date_object.isoformat()
    return date_object


def check_language(language):
    """Check if a language code or object is correct"""
    if isinstance(language, (list, tuple)):
        return flat([check_language(item) for item in language])
    if language == 'xx': return ['xx']
    if language == 'zh': return ['zh-cn', 'zh-tw']
    if language in ['zh-cn', 'zh-tw']:
        return [language]
    try:
        ans = pycountry.languages.lookup(language).alpha_2
    except LookupError:
        raise ValueError("{} is an unknown language code.".format(
            language
        ))
    return [ans]


def check_geocode(country):
    """Check if a country code or object is correct"""
    if isinstance(country, (list, tuple)):
        return [check_geocode(item) for item in country]
    if country == 'xx': return 'xx'
    try:
        ans = pycountry.countries.lookup(country).alpha_2
    except LookupError:
        raise ValueError("{} is an unknown geographical code.".format(
            country
        ))
    return ans


def check_list(elements, rtype, assertion_message=None):
    """Check if all the items of a list has the right type"""
    error_message = "Invalid type (must be a list of {})".format(rtype)
    assertion_message = assertion_message or error_message
    assert isinstance(elements, list), 'A list must be given.'
    assert all([isinstance(element, rtype) for element in elements]), \
        assertion_message
    return None
