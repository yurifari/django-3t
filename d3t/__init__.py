from pkg_resources import DistributionNotFound, get_distribution

from d3t.watcher import watch

__all__ = [
    'watch',
]

DISTRIBUTION_NAME = 'django-3t'

try:
    __version__ = get_distribution(DISTRIBUTION_NAME).version
except DistributionNotFound:
    pass
