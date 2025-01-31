# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import sys
from azure.iot.device.provisioning.pipeline import pipeline_ops_provisioning
from tests.common.pipeline import pipeline_data_object_test

this_module = sys.modules[__name__]

pipeline_data_object_test.add_operation_test(
    cls=pipeline_ops_provisioning.SetSymmetricKeySecurityClientOperation,
    module=this_module,
    positional_arguments=["security_client"],
    keyword_arguments={"callback": None},
)
pipeline_data_object_test.add_operation_test(
    cls=pipeline_ops_provisioning.SetSecurityClientArgsOperation,
    module=this_module,
    positional_arguments=["provisioning_host", "registration_id", "id_scope"],
    keyword_arguments={"callback": None},
)
pipeline_data_object_test.add_operation_test(
    cls=pipeline_ops_provisioning.SendRegistrationRequestOperation,
    module=this_module,
    positional_arguments=["request_id", "request_payload"],
    keyword_arguments={"callback": None},
    extra_defaults={"needs_connection": True},
)
pipeline_data_object_test.add_operation_test(
    cls=pipeline_ops_provisioning.SendQueryRequestOperation,
    module=this_module,
    positional_arguments=["request_id", "operation_id", "request_payload"],
    keyword_arguments={"callback": None},
    extra_defaults={"needs_connection": True},
)
