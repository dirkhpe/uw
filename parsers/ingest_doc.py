"""
This script loads a document for preprocessing in Apache Tika before indexing in Elastic.
"""
import argparse
import logging
from lib import elasticlib
from lib import my_env

# Configure command line arguments
parser = argparse.ArgumentParser(
    description="Create an index."
)
parser.add_argument('-i', '--index', type=str, required=True,
                    help='Please provide the name of the index.')
parser.add_argument('-f', '--file', type=str, required=True,
                    help='Please provide the file for indexing.')
args = parser.parse_args()
cfg = my_env.init_env("elasticload", __file__)
el = elasticlib.Elastic()
logging.info("Arguments: {a}".format(a=args))
el.post_tika(args.index, args.file)
