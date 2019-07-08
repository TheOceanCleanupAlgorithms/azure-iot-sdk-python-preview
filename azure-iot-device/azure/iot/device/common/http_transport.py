# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import requests


class HTTPTransport(object):
    """
    Class providing an generic HTTP request interface
    """

    def post(self, url, data):
        """
        Make an HTTP POST request
        """
        requests.post(url, data=data)
