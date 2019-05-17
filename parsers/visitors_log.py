"""
This script will load visitor database into elasticsearch.
"""

import geoip2.database
from lib import elasticlib
from lib import localstore
from lib import my_env
import json
import logging


def add_location(ip):
    """
    This method will add lat and lon coordinates to the iploc dictionary for the IP.

    :param ip: IP address for which lat and lon are required
    :return:
    """
    try:
        res = geoipdb.city(ip)
    except geoip2.errors.AddressNotFoundError:
        iploc[ip] = dict(
            lat=0,
            lon=0
        )
        logging.error("IP Address {ip} not found in GeoIP Database".format(ip=ip))
    else:
        if res.location.latitude:
            iploc[ip] = dict(
                lat=res.location.latitude,
                lon=res.location.longitude
            )
        else:
            iploc[ip] = dict(
                lat=0,
                lon=0
            )
            logging.error("IP Address {ip} found in GeoIP Database but no lat/long coordinates".format(ip=ip))
    return


cfg = my_env.init_env("elasticload", __file__)
lcl = localstore.SqliteUtils("visitors.db")
el = elasticlib.Elastic()
geoipdb = geoip2.database.Reader("c:/development/python/elastic/data/GeoLite2-City.mmdb")
iploc = {}


# Collect User Agent information
agent = {}
records = lcl.get_table("useragents")
lc = my_env.LoopInfo("User Agents Records", 20)
for trow in records:
    row = dict(trow)
    agent[row["id"]] = row

records = lcl.get_table("requests")
lc = my_env.LoopInfo("Visitor Records", 100)
for trow in records:
    row = dict(trow)
    row["agent"] = agent[row["uagent_id"]]
    try:
        row["location"] = dict(
            lat=iploc[row["hostip"]]["lat"],
            lon=iploc[row["hostip"]]["lon"]
        )
    except KeyError:
        add_location(row["hostip"])
        row["location"] = dict(
            lat=iploc[row["hostip"]]["lat"],
            lon=iploc[row["hostip"]]["lon"]
        )
    el.post_document('vislog', json.dumps(row))
    cnt = lc.info_loop()
    """
    if cnt > 1000:
        break
    """
lc.end_loop()
