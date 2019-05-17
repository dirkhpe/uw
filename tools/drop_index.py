"""
This script will drop an index in elasticsearch.
"""

from lib import elasticlib
from lib import my_env
import argparse
import logging
import pprint

# Configure command line arguments
parser = argparse.ArgumentParser(
    description="Drop an index."
)
parser.add_argument('-i', '--index', type=str, required=True,
                    help='Please provide the name of the index.')
args = parser.parse_args()
cfg = my_env.init_env("elasticload", __file__)
pp = pprint.PrettyPrinter(indent=4)
el = elasticlib.Elastic()
logging.info("Arguments: {a}".format(a=args))

index = args.index
res = el.delete_index(index)
pp.pprint(res.content)
