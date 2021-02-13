from pkg_resources import get_distribution, DistributionNotFound
from justic.core import Justic

__all__ = ['Justic']

try:
    __version__ = get_distribution('justic').version
except:
    __version__ = 'unknown'
finally:
    del get_distribution, DistributionNotFound
