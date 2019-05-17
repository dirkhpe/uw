"""
This script will create an new index in elasticsearch. Use script 'add_mapping.py' to add mapping.
"""

from lib import elasticlib
from lib import my_env
import argparse
import json
import logging
import pprint

# Configure command line arguments
parser = argparse.ArgumentParser(
    description="Create an index."
)
parser.add_argument('-i', '--index', type=str, required=True,
                    help='Please provide the name of the index.')
parser.add_argument('-m', '--mapfile', type=str, required=False,
                    help='Please provide mapping file (Optionally)')
args = parser.parse_args()
cfg = my_env.init_env("elasticload", __file__)
pp = pprint.PrettyPrinter(indent=4)
el = elasticlib.Elastic()
logging.info("Arguments: {a}".format(a=args))

index = args.index
if args.mapfile:
    fn = args.mapfile
    with open(fn) as json_file:
        mapping = json.load(json_file)
    data = dict(mappings=mapping)
    res = el.put_index(index, json.dumps(data))
else:
    res = el.put_index(index)
print("Create index {index}: ".format(index=index))
pp.pprint(res.json())
