"""
Used to color some logs.
"""


class COLOR:
    """Settings for color in terminal"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def blue(string):
    """Convert a string into a string with blue font"""
    return '{}{}{}'.format(COLOR.OKBLUE, string, COLOR.ENDC)


def green(string):
    """Convert a string into a string with green font"""
    return '{}{}{}'.format(COLOR.OKGREEN, string, COLOR.ENDC)


def red(string):
    """Convert a string into a string with red font"""
    return '{}{}{}'.format(COLOR.FAIL, string, COLOR.ENDC)
