#!/usr/local/env python
# -*- coding: utf-8 -*-
"""Python Library for Interfacing with the LendingClub API

Copyright (c) 2015 Pete Morici

This modules provides an easy way to use the LendingClub API through Python.

"""
import json
from datetime import datetime
from httplib import HTTPSConnection
from posixpath import join as urljoin
from ssl import create_default_context, Purpose

class Client(object):
    """LendingClub API client

    """

    def __init__(self, investor_id, api_key, api_version='v1', 
                 host='api.lendingclub.com', path='/api/investor'):
        """Connection to LendingClub API.  
        
        Each client requires an `investor_id` and `api_key`.  All other 
        arguments are optional.

        Args:
          investor_id (int): The accounts Investor Id this can be found on the 
            Account Summary page on the LendingClub website after loging in.
          api_key (str): Account authorization token found under Settings.
          api_version (str, optional): api version endpoint.
          host (str, optional): Host name of api endpoint.
          path (str, optional): Base path of api endpoint.
        
        """
        self._last_update = None
        self._host = host
        investor_id = str(investor_id)
        self._investor_id = investor_id
        self._base_path = urljoin(path, api_version)
        self._acct_path = urljoin(self._base_path, 'accounts', investor_id) 
        self._loan_path = urljoin(self._base_path, 'loans')

        self._default_headers = {'Authorization': api_key,
                                 'Accept': 'application/json',
                                 'Content-type': 'application/json'}

        ssl_ctx = create_default_context(Purpose.SERVER_AUTH)
        self._conn = HTTPSConnection(host, context=ssl_ctx)
        self._conn.set_debuglevel(10)

        self._conn.connect()

    def __del__(self):
        self._conn.close()

    def summary(self):
        """Return a dict object summarizing account data"""
        request_url = urljoin(self._acct_path, 'summary')
        self._conn.request('GET', request_url, None, self._default_headers)

        r = self._conn.getresponse()

        return json.load(r)

    def loans(self):
        """
        """
        request_url = urljoin(self._loan_path, 'listing')
        self._conn.request('GET', request_url, None, self._default_headers)

        r = self._conn.getresponse()

        data = json.load(r)
        self._last_update = data['asOfDate']

        return data['loans']

    def last_update(self):
        """Get the date / time the loan data was last updated.
        Returns:
          datetime: timestamp of last loan data update.
        """
        return self._last_update

if __name__ == '__main__':
    import os
    import sys

    investor_id = int(sys.argv[1])
    api_key = os.environ['LC_API_KEY']

    lc_client = Client(investor_id, api_key)

    print lc_client.loans()[0]
    print lc_client.last_update()
    print lc_client.summary()
