import json
import locale
import logging
import os
import gui.lib.requests_wrapper as rw
from operator import itemgetter

locale.setlocale(locale.LC_ALL, '')


class Elastic:

    def __init__(self):
        self.host = os.getenv("ELASTIC_HOST")
        self.port = os.getenv("ELASTIC_PORT")
        self.url_elastic = "http://{host}:{port}".format(host=self.host, port=self.port)
        self.headers = {'Content-Type': 'application/json; charset=utf-8', 'Accept': 'application/json'}

    def get_indices(self, purpose=None):
        """
        This method will return the indices known in Elasticsearch.

        :param purpose: Purpose of the call. None: returns every index and all associated information. forSelect:
        returns sorted list of user indices. A user index is an index that does not start with . (dot).
        :return: Result of the GET /_cat/indices?v call or list with user index value pairs.
        """
        url = "{url_home}/{function}/indices?v".format(url_home=self.url_elastic, function="_cat")
        res = rw.get(url, headers=self.headers)
        if purpose == 'forSelect':
            # Convert result to list of user index pairs
            lbl = 'index'
            user_indices = [(ind[lbl], '{} ({:n})'.format(ind[lbl], int(ind['docs.count'])))
                            for ind in res.json() if (ind[lbl][0] != '.') and (int(ind['docs.count']) > 0)]
            user_indices.sort(key=itemgetter(0))
            return user_indices
        return res

    def get_mapping(self, index):
        """
        This method will return the mapping for a specific index.

        :param index: Index for which the mapping needs to be retrieved.
        :return: Result of the GET /{index}/_mapping call.
        """
        url = "{url_home}/{index}/{function}".format(url_home=self.url_elastic, index=index, function="_mapping")
        res = rw.get(url, headers=self.headers)
        return res

    def search_for(self, indexname, field, term, outfield=None):
        """
        This method will search for term in field of indexname. Output fields are listed in outfield.
        :param indexname: Name of the index to search.
        :param field: Field of the index that needs to be searched.
        :param term: Term that will be searched in the index
        :param outfield: (optional) list of fields to include in the response.
        :return: Result of the search query.
        """
        url = "{url_home}/{index}/{function}".format(url_home=self.url_elastic, index=indexname, function="_search")
        match = {field: dict(query=term)}
        data = dict(
            query=match
        )
        res = rw.get(url, headers=self.headers, data=json.dumps(data))
        return res


propdict = {}


def map2list(mapping):
    """
    This method gets a mapping dictionary and converts is to a map list. A map list lists the property names and field
    types. See lkb for structure of the mapping file.

    :param mapping: Dictionary of the index mapping.
    :return: List of tuples (indexname, indexname + type per field) for usage in SelectField or RadioField
    """
    # Check on mapping dictionary, with size=1:
    if not isinstance(mapping, dict):
        logging.error("Mapping type not dictionary but {}".format(type(mapping)))
        return None, None
    if len(mapping) != 1:
        logging.error("Mapping dictionary unexpected length {}, should be 1".format(len(mapping)))
        return None, None
    index = list(mapping.keys())[0]
    props = mapping[index]['mappings']['properties']
    itermap("", props)
    # Remove first dot in each property name
    proplist = []
    for k, v in sorted(propdict.items()):
        k = k[1:]
        proplist.append((k, "{} {}".format(k, v)))
    return proplist


def itermap(parent, indexmap):
    """
    This function recursively walks through the index map to extract properties and add them to a dictionary.

    :param parent: parent property of this property
    :param indexmap: part of the index map that is analyzed.
    :return:
    """
    for k, v in indexmap.items():
        if not isinstance(v, dict):
            logging.fatal("Property {k} description not dictionary: {v} ".format(k=k, v=v))
            return
        prop = "{}.{}".format(parent, k)
        if "type" in v:
            if "fields" in v:
                embedded_map = v["fields"]
                itermap(prop, embedded_map)
                del v["fields"]
            propdict[prop] = v
        elif "properties" in v:
            if len(v) != 1:
                logging.fatal("Embedded properties of {} not in dictionary with length 1: {}".format(k, v))
                return
            embedded_map = v["properties"]
            itermap(prop, embedded_map)
    return
