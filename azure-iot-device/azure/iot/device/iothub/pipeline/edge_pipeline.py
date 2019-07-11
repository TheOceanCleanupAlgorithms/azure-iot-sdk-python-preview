# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import logging
from azure.iot.device.common.pipeline import pipeline_stages_base, pipeline_stages_http
from . import pipeline_ops_edge, pipeline_stages_edge, pipeline_stages_edge_http

logger = logging.getLogger(__name__)


class EdgePipeline(object):
    """Pipeline to communicate with Edge.
    Uses HTTP.
    """

    def __init__(self, auth_provider):
        self._pipeline = (
            pipeline_stages_base.PipelineRootStage()
            .append_stage(pipeline_stages_edge.UseAuthProviderStage())
            .append_stage(pipeline_stages_edge_http.EdgeHTTPConverterStage())
            .append_stage(pipeline_stages_http.HTTPTransportStage())
        )

        # TODO: something really needs to be done about this
        # It's been hanging around for far too long
        def remove_this_code(call):
            if call.error:
                raise call.error

        self._pipeline.run_op(
            pipeline_ops_edge.SetAuthProviderOperation(
                auth_provider=auth_provider, callback=remove_this_code
            )
        )

    def invoke_device_method(self):
        pass

    def invoke_module_method(self):
        pass
