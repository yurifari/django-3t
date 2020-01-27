from pkg_resources import DistributionNotFound, get_distribution

DISTRIBUTION_NAME = 'django-3t'

try:
    __version__ = get_distribution(DISTRIBUTION_NAME).version
except DistributionNotFound:
    pass
