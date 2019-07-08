# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


import logging
from azure.iot.device.common.pipeline import PipelineStage
from . import pipeline_ops_edge

logger = logging.getLogger(__name__)


class EdgeHTTPConverterStage(PipelineStage):
    def __init__(self):
        super(EdgeHTTPConverterStage, self).__init__()

    def _run_op(self, op):

        if isinstance(op, pipeline_ops_edge.InvokeMethodOperation):
            # data = {"methodName": op.method_name, "timeout": op.timeout, "payload": op.payload}
            pass
