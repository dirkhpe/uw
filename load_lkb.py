"""
This script will load lkb database into elasticsearch.
"""

from lib import elasticlib
from lib import localstore
from lib import my_env
import json

cfg = my_env.init_env("elasticload", __file__)
lcl = localstore.SqliteUtils()
el = elasticlib.Elastic()

# Collect parent titles
parents = {}
query = "SELECT distinct(parent_id) from node where parent_id > 0"
res = lcl.get_query(query)
for rec in res:
    query = "SELECT title from node where nid={parent_id}".format(parent_id=rec["parent_id"])
    title_res = lcl.get_query(query)
    parents[str(rec["parent_id"])] = title_res[0]["title"]


records = lcl.get_table("node")
lc = my_env.LoopInfo("lkb Records", 20)
for trow in records:
    row = dict(trow)
    try:
        row["parent"] = parents[str(row["parent_id"])]
    except KeyError:
        pass
    el.post_document('lkb', json.dumps(row))
    cnt = lc.info_loop()
lc.end_loop()
