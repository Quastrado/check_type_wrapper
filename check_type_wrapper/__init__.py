from .check_type import check_type
from .discrepancy_item import DiscrepancyItem
from .exception import TypeMissMatchException

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
