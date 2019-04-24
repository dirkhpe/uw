"""
This script will get the indices in elasticsearch.
"""

from lib import elasticlib
from lib import my_env
import pprint

cfg = my_env.init_env("elasticload", __file__)
pp = pprint.PrettyPrinter()
el = elasticlib.Elastic()
res = el.get_indices()
pp.pprint(res.json())

