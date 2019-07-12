# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import logging
from azure.iot.device.common.pipeline import PipelineStage, operation_flow, pipeline_ops_http
from . import pipeline_ops_edge

logger = logging.getLogger(__name__)


# If this section for URLS gets expanded, consider moving to a separate module
# like was done for MQTT in mqtt_topic_iothub.py
EDGE_API_VERSION = "2018-06-27"


def get_url_for_method_invoke(device_id, module_id=None):
    url = "/twins/" + device_id
    if module_id:
        url += "/modules/" + module_id
    url += "/methods"
    return url


class EdgeHTTPConverterStage(PipelineStage):
    def __init__(self):
        super(EdgeHTTPConverterStage, self).__init__()

    def _run_op(self, op):
        if isinstance(op, pipeline_ops_edge.SetAuthProviderArgsOperation):

            operation_flow.delegate_to_different_op(
                stage=self,
                original_op=op,
                new_ope=pipeline_ops_http.SetHTTPConnectionArgsOperation(
                    hostname=op.gateway_hostname, ca_cert=op.ca_cert  # Talking to Edge
                ),
            )

        if isinstance(op, pipeline_ops_edge.InvokeMethodOperation):
            data = {"methodName": op.method_name, "timeout": op.timeout, "payload": op.payload}
            params = {"api-version": EDGE_API_VERSION}
            url = get_url_for_method_invoke(op.device_id, op.module_id)
            operation_flow.delegate_to_different_op(
                stage=self,
                original_op=op,
                new_op=pipeline_ops_http.HTTPPostOperation(url=url, params=params, data=data),
            )
        else:
            # All other operations get passed down
            operation_flow.pass_op_to_next_stage(self, op)
