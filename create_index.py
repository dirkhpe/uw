"""
This script will create an new index in elasticsearch. Use script 'add_mapping.py' to add mapping.
"""

from lib import elasticlib
from lib import my_env
import argparse
import logging
import pprint

# Configure command line arguments
parser = argparse.ArgumentParser(
    description="Create an index."
)
parser.add_argument('-i', '--index', type=str, required=True,
                    help='Please provide the name of the index.')
args = parser.parse_args()
cfg = my_env.init_env("elasticload", __file__)
pp = pprint.PrettyPrinter(indent=4)
el = elasticlib.Elastic()
logging.info("Arguments: {a}".format(a=args))

index = args.index
res = el.put_index(index)
print("Create index {index}: ".format(index=index))
pp.pprint(res.json())
