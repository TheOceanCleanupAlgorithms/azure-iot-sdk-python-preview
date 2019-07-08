# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import logging
from azure.iot.device.common.pipeline import pipeline_stages_base
from . import pipeline_ops_edge

logger = logging.getLogger(__name__)


class EdgePipeline(object):
    """Pipeline to communicate with Edge.
    Uses HTTP.
    """

    def __init__(self):
        self._pipeline = pipeline_stages_base.PipelineRootStage()

    def invoke_device_method(self):
        pass

    def invoke_module_method(self):
        pass
