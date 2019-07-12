# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from . import PipelineOperation


# TODO: revist naming
class SetHTTPConnectionArgsOperation(PipelineOperation):
    """
    A PipelineOperation object which contains data used to connect to a server using the HTTP protocol.

    This operation is in the group of HTTP operations because it is specific to the HTTP protocol.
    """

    def __init__(self, hostname, ca_cert=None, callback=None):
        super(SetHTTPConnectionArgsOperation, self).__init__(callback=callback)
        self.hostname = hostname
        self.ca_cert = ca_cert


class HTTPPostOperation(PipelineOperation):
    """
    A PipelineOperation object which contains data used to make a POST request.

    This operation is in the group of HTTP operations because it is specific to the HTTP protocol.
    """

    def __init__(self, url, params=None, data=None, callback=None):
        super(HTTPPostOperation, self).__init__(callback=callback)
        self.url = url
        self.params = params
        self.data = data
