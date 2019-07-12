# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import logging
from azure.iot.device.common.http_transport import HTTPTransport
from . import PipelineStage, pipeline_ops_http

logger = logging.getLogger(__name__)


class HTTPTransportStage(PipelineStage):
    """
    PipelineStage object which is responsible for interfacing with the HTTPTransport.
    This stage handles all HTTP operations
    """

    def _run_op(self, op):
        if isinstance(op, pipeline_ops_http.HTTPPostOperation):
            logger.info("")
