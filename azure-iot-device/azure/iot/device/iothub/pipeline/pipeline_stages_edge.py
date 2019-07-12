# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import logging
from azure.iot.device.common.pipeline import PipelineStage, pipeline_ops_edge, operation_flow


logger = logging.getLogger(__name__)


class UseAuthProviderStage(PipelineStage):
    def _run_op(self, op):

        if isinstance(op, pipeline_ops_edge.SetAuthProviderOperation):
            # TODO: some kind of verification of the right type of auth provider
            # Until then, just assume this is an IoTEdgeAuthenticationProvider
            auth_provider = op.auth_provider
            operation_flow.delegate_to_different_op(
                stage=self,
                original_op=op,
                new_op=pipeline_ops_edge.SetAuthProviderArgsOperation(
                    gateway_hostname=auth_provider.gatewayhostname, ca_cert=auth_provider.ca_cert
                ),
            )
        else:
            operation_flow.pass_op_to_next_stage(self, op)
