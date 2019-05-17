"""
This script will get the number of documents in an index.
"""

from lib import elasticlib
from lib import my_env
import argparse
import logging
import pprint

# Configure command line arguments
parser = argparse.ArgumentParser(
    description="Find number of documents for an index."
)
parser.add_argument('-i', '--index', type=str, required=True,
                    help='Please provide the name of the index.')
args = parser.parse_args()
cfg = my_env.init_env("elasticload", __file__)
logging.info("Arguments: {a}".format(a=args))

pp = pprint.PrettyPrinter(indent=4)
el = elasticlib.Elastic()
index = args.index
res = el.get_count(index)
print("Count information for index {index}".format(index=index))
pp.pprint(res.json())
