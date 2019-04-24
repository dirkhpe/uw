"""
This function is a wrapper for the requests library.
An instance of the class will accept input values, execute the call and check on return code. If successful, result
content will be returned. Otherwise an error message is added to the logfile.
"""

import logging
import requests


def delete(url, headers):
    """
    Issue a Delete Requests. Input parameters are url and headers for now.

    :param url:
    :param headers:
    :return: Result of the Delete, or HTTPError in case of status_code != 200.
    """
    r = requests.delete(url, headers=headers)
    if r.status_code == 200:
        msg = "DELETE OK - URL: {url}, Headers: {headers}".format(url=url, headers=headers)
        logging.debug(msg)
        return r
    else:
        msg = "DELETE NOT OK, Return status: {code} - URL: {url}, Headers: {headers}".format(url=url, headers=headers,
                                                                                             code=r.status_code)
        logging.error(msg)
        logging.error(r.content)
        r.raise_for_status()
        return


def get(url, headers):
    """
    Issue a Get Requests. Input parameters are url and headers for now.

    :param url:
    :param headers:
    :return: Result of the GET, or HTTPError in case of status_code != 200.
    """
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        msg = "GET OK - URL: {url}, Headers: {headers}".format(url=url, headers=headers)
        logging.debug(msg)
        return r
    else:
        msg = "GET NOT OK, Return status: {code} - URL: {url}, Headers: {headers}".format(url=url, headers=headers,
                                                                                          code=r.status_code)
        logging.error(msg)
        logging.error(r.content)
        r.raise_for_status()
        return


def post(url, headers, **kwargs):
    """
    Issue a Post request. Input parameters are url, headers and data.

    :param url: POST URL (mandatory)
    :param headers: headers are mandatory
    :param kwargs: additional attributes. Typically it will have a data= attribute.
    :return:
    """
    r = requests.post(url, headers=headers, **kwargs)
    if r.status_code == 200:
        msg = "POST OK - URL: {url}, Headers: {headers}".format(url=url, headers=headers)
        logging.debug(msg)
        return r
    else:
        msg = "POST NOT OK, Return status: {code} - URL: {url}, Headers: {headers}".format(url=url, headers=headers,
                                                                                          code=r.status_code)
        logging.error(msg)
        logging.error(r.content)
        r.raise_for_status()
        return


def put(url, headers, **kwargs):
    """
    Issue a Put request. Input parameters are url, headers and data.

    :param url: PUT URL (mandatory)
    :param headers: headers are mandatory
    :param kwargs: additional attributes. Typically it will have a data= attribute.
    :return:
    """
    r = requests.put(url, headers=headers, **kwargs)
    if r.status_code == 200:
        msg = "PUT OK - URL: {url}, Headers: {headers}".format(url=url, headers=headers)
        logging.debug(msg)
        return r
    else:
        msg = "PUT NOT OK, Return status: {code} - URL: {url}, Headers: {headers}".format(url=url, headers=headers,
                                                                                          code=r.status_code)
        logging.error(msg)
        logging.error(r.content)
        r.raise_for_status()
        return
