"""
This script will get the mapping for an index.
"""

from lib import elasticlib
from lib import my_env
import argparse
import logging
import pprint

# Configure command line arguments
parser = argparse.ArgumentParser(
    description="Get mapping for an index."
)
parser.add_argument('-i', '--index', type=str, required=True,
                    help='Please provide the name of the index.')
args = parser.parse_args()
cfg = my_env.init_env("elasticload", __file__)
pp = pprint.PrettyPrinter(indent=4)
logging.info("Arguments: {a}".format(a=args))

index = args.index
el = elasticlib.Elastic()
res = el.get_mapping(index)
pp.pprint(res.json())

proplist = elasticlib.map2list(res.json())
for k, v in sorted(proplist.items()):
    print("{}: {}".format(k, v))
