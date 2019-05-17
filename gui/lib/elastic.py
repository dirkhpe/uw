import os
import gui.lib.requests_wrapper as rw


class Elastic:

    def __init__(self):
        self.host = os.getenv("ELASTIC_HOST")
        self.port = os.getenv("ELASTIC_PORT")
        self.url_elastic = "http://{host}:{port}".format(host=self.host, port=self.port)
        self.headers = {'Content-Type': 'application/json; charset=utf-8', 'Accept': 'application/json'}

    def get_indices(self):
        """
        This method will return the indices known in Elasticsearch.

        :return: Result of the GET /_cat/indices?v call.
        """
        url = "{url_home}/{function}/indices?v".format(url_home=self.url_elastic, function="_cat")
        res = rw.get(url, headers=self.headers)
        return res
