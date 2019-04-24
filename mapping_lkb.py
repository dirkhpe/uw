"""
This script will put the mapping for the lkb-index.
"""

from lib import elasticlib
from lib import my_env
import pprint

cfg = my_env.init_env("elasticload", __file__)
pp = pprint.PrettyPrinter(indent=4)
el = elasticlib.Elastic()
res = el.put_map('lkb')
pp.pprint(res.json())
