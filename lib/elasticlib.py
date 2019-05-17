"""
The purpose of this module is to generate JSON structures for communication with elastic.
"""

# import logging
import json
import os
import lib.requests_wrapper as rw
from base64 import b64encode


class Elastic:

    def __init__(self):
        self.host = os.getenv("ELASTIC_HOST")
        self.port = os.getenv("ELASTIC_PORT")
        self.url_elastic = "http://{host}:{port}".format(host=self.host, port=self.port)
        self.headers = {'Content-Type': 'application/json; charset=utf-8', 'Accept': 'application/json'}

    def delete_index(self, index):
        """
        This method will drop the specific index.

        :param index: Index to be removed.
        :return: Result of the DELETE /{index} call.
        """
        url = "{url_home}/{index}".format(url_home=self.url_elastic, index=index)
        res = rw.delete(url, headers=self.headers)
        return res

    def get_count(self, index):
        """
        This method will return the number of documents for a specific index.

        :param index: Index for which the number of documents need to be created.
        :return: Result of the GET /{index}/_count call.
        """
        url = "{url_home}/{index}/{function}".format(url_home=self.url_elastic, index=index, function="_count")
        res = rw.get(url, headers=self.headers)
        return res

    def get_health(self):
        """
        This method will return the health of Elasticsearch server.

        :return: Result of the GET /_cat/health?v call.
        """
        url = "{url_home}/{function}/health?v".format(url_home=self.url_elastic, function="_cat")
        res = rw.get(url, headers=self.headers)
        return res

    def get_indices(self):
        """
        This method will return the indices known in Elasticsearch.

        :return: Result of the GET /_cat/indices?v call.
        """
        url = "{url_home}/{function}/indices?v".format(url_home=self.url_elastic, function="_cat")
        res = rw.get(url, headers=self.headers)
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

    def get_version(self):
        """
        This method will return the version of Elasticsearch server.

        :return: Result of the GET / call.
        """
        url = "{url_home}/".format(url_home=self.url_elastic)
        res = rw.get(url, headers=self.headers)
        return res

    def post_document(self, index, document):
        """
        This method will add a document to the index. The document ID will be calculated by Elasticsearch.

        :param index: Name of the index
        :param document: Document to be added to the index as a json formatted string.
        :return:
        """
        url = "{url_home}/{index}/{function}".format(url_home=self.url_elastic, index=index, function="_doc")
        res = rw.post(url, headers=self.headers, data=document)
        return res

    def post_tika(self, index, fn):
        """
        This method will parse a file with Apache Tika, then post to the index. The document ID will be calculated by
        Elasticsearch.

        :param index: Name of the index
        :param fn: Full filename of the document to be parsed and added to the index.
        :return:
        """
        fh = open(fn, mode='rb')
        content = fh.read()
        doc_dict = dict(data=b64encode(content).decode("utf-8"))
        document = json.dumps(doc_dict)
        url = "{url_home}/{index}/{function}?pipeline=attachment".format(url_home=self.url_elastic,
                                                                         index=index, function="_doc")
        res = rw.post(url, headers=self.headers, data=document)
        return res

    def put_index(self, index, mapping=None):
        """
        This method will create an index in elasticsearch.

        :param index: Name of the index
        :param mapping: json formatted string containing mapping information (optional)
        :return:
        """
        url = "{url_home}/{index}".format(url_home=self.url_elastic, index=index)
        res = rw.put(url, headers=self.headers, data=mapping)
        return res

    def put_mapping(self, index, mapping):
        """
        This method will create the index mapping.

        :param index: Name of the index for which mapping is provided.
        :param mapping: json formatted string containing mapping information
        :return:
        """
        url = "{url_home}/{index}/{function}".format(url_home=self.url_elastic, index=index, function="_mapping")
        res = rw.put(url, headers=self.headers, data=mapping)
        return res
