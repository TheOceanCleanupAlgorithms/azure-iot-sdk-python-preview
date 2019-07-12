# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from azure.iot.device.common.pipeline import PipelineOperation


# TODO: unify this with the one in iothub
class SetAuthProviderOperation(PipelineOperation):
    def __init__(self, auth_provider, callback=None):
        super(SetAuthProviderOperation, self).__init__(callback=callback)
        self.auth_provider = auth_provider


# TODO: Resolve overlap with the one in iothub. These probably can't be shared.
# But a more meaningful (and notably, endpoint specific) name might help.
# Also worth considering if there's even a point to having this operation separate
# from the above one - why have a separate stage just to extract the properties from the
# auth provider?
# Argument for having it -> separation of concern, only pass the minimum values required
# In this case, Edge auth gives us lots of fields we don't need (e.g. hostname, device id, etc.)
class SetAuthProviderArgsOperation(PipelineOperation):
    def __init__(self, gateway_hostname, ca_cert, callback=None):
        super(SetAuthProviderArgsOperation, self).__init__(callback=callback)
        # No need for hostname when talking to the Edge endpoint.
        # GatewayHostname and CA cert are REQUIRED for the Edge endpoint.
        self.gateway_hostname
        self.ca_cert = ca_cert


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
