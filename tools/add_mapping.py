"""
This script will add mapping to an index in elasticsearch.
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
parser.add_argument('-f', '--file', type=str, required=True,
                    help='Please provide the file containing mappings in json format')
args = parser.parse_args()
cfg = my_env.init_env("elasticload", __file__)
pp = pprint.PrettyPrinter(indent=4)
el = elasticlib.Elastic()
logging.info("Arguments: {a}".format(a=args))

index = args.index
fn = args.file
with open(fn) as json_file:
    mapping = json.load(json_file)
data = dict(properties=mapping)
res = el.put_mapping(index, json.dumps(data))
print("Add mapping for index {index}".format(index=index))
pp.pprint(res.json())
