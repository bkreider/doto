from __future__ import print_function, division, absolute_import
import requests

from doto.exceptions import DOError
from doto.logger import log

BASEURL = "https://api.digitalocean.com"

class connection(object):
    def __init__(self, client_id, api_key):
        self.__client_id = client_id
        self.__api_key = api_key

    def __repr__(self):
        return "connection()"

    __str__ = __repr__

    def request(self, event, status_check=False, **kwds):
            if 'client_id' not in kwds:
                kwds['client_id'] = self.__client_id
            if 'api_key' not in kwds:
                kwds['api_key'] = self.__api_key

            headers = {
                'User-Agent': 'doto/client'
            }

            for key, value in kwds.iteritems():
                log.debug("%s = %s" % (key, value))

            response = requests.get(BASEURL+event,headers=headers,params=kwds)
            log.info('Getting '+event)
            log.debug(response.url)

            if response.status_code == 200:
                data = response.json()
                log.debug(data)

                if data['status'] == 'ERROR':
                    log.debug("Error with request: %s" % (data['message']))
                    error = "MSG: %s" % (data['message'])
                    raise DOError(error)

                if status_check:
                    return response.status_code

                return data
            else:
                #error
                # fixme
                data = dict(message="fake message")
                error = "Status code: %d MSG: %s" % (response.status_code, data['message'])
                raise DOError(error)
