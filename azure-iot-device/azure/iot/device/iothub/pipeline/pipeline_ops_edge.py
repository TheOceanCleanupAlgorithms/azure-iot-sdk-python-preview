# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from azure.iot.device.common.pipeline import PipelineOperation


class InvokeMethodOperation(PipelineOperation):
    """
    A PipelineOperation object which contains the required information to invoke a method on
    a Device or a Module via Edge.

    This operation is in the group of Edge operations because it is specific to Edge.
    """

    def __init__(self, device_id, module_id, method_name, payload, timeout, callback):
        super(InvokeMethodOperation, self).__init__(callback=callback)
        self.device_id = device_id
        self.module_id = module_id
        self.method_name = method_name
        self.payload = payload
        self.timeout = timeout
