# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import logging
from azure.iot.device.common.pipeline import (
    pipeline_stages_base,
    pipeline_ops_base,
    pipeline_stages_mqtt,
)
from . import (
    constant,
    pipeline_stages_iothub,
    pipeline_events_iothub,
    pipeline_ops_iothub,
    pipeline_stages_iothub_mqtt,
)
from azure.iot.device.iothub.auth.x509_authentication_provider import X509AuthenticationProvider

logger = logging.getLogger(__name__)


class IoTHubPipeline(object):
    def __init__(self, auth_provider):
        """
        Constructor for instantiating a pipeline adapter object
        :param auth_provider: The authentication provider
        """
        self._auth_provider = auth_provider
        self.feature_enabled = {
            constant.C2D_MSG: False,
            constant.INPUT_MSG: False,
            constant.METHODS: False,
            constant.TWIN: False,
            constant.TWIN_PATCHES: False,
        }

        # Event Handlers - Will be set by Client after instantiation of this object
        self.on_connected = None
        self.on_disconnected = None
        self.on_c2d_message_received = None
        self.on_input_message_received = None
        self.on_method_request_received = None
        self.on_twin_patch_received = None

        self._pipeline = (
            pipeline_stages_base.PipelineRootStage()
            .append_stage(pipeline_stages_iothub.UseAuthProviderStage())
            .append_stage(pipeline_stages_iothub.HandleTwinOperationsStage())
            .append_stage(pipeline_stages_base.CoordinateRequestAndResponseStage())
            .append_stage(pipeline_stages_base.EnsureConnectionStage())
            .append_stage(pipeline_stages_iothub_mqtt.IoTHubMQTTConverterStage())
            .append_stage(pipeline_stages_mqtt.MQTTClientStage())
        )

        def _handle_pipeline_event(event):
            if isinstance(event, pipeline_events_iothub.C2DMessageEvent):
                if self.on_c2d_message_received:
                    self.on_c2d_message_received(event.message)
                else:
                    logger.warning("C2D event received with no handler.  dropping.")

            elif isinstance(event, pipeline_events_iothub.InputMessageEvent):
                if self.on_input_message_received:
                    self.on_input_message_received(event.input_name, event.message)
                else:
                    logger.warning("input mesage event received with no handler.  dropping.")

            elif isinstance(event, pipeline_events_iothub.MethodRequestEvent):
                if self.on_method_request_received:
                    self.on_method_request_received(event.method_request)
                else:
                    logger.warning("Method request event received with no handler. Dropping.")

            elif isinstance(event, pipeline_events_iothub.TwinDesiredPropertiesPatchEvent):
                if self.on_twin_patch_received:
                    self.on_twin_patch_received(event.patch)
                else:
                    logger.warning("Twin patch event received with no handler. Dropping.")

            else:
                logger.warning("Dropping unknown pipeline event {}".format(event.name))

        def _handle_connected():
            if self.on_connected:
                self.on_connected("connected")

        def _handle_disconnected():
            if self.on_disconnected:
                self.on_disconnected("disconnected")

        self._pipeline.on_pipeline_event = _handle_pipeline_event
        self._pipeline.on_connected = _handle_connected
        self._pipeline.on_disconnected = _handle_disconnected

        def remove_this_code(call):
            if call.error:
                raise call.error

        if isinstance(auth_provider, X509AuthenticationProvider):
            op = pipeline_ops_iothub.SetX509AuthProviderOperation(
                auth_provider=auth_provider, callback=remove_this_code
            )
        else:  # Currently everything else goes via this block.
            op = pipeline_ops_iothub.SetAuthProviderOperation(
                auth_provider=auth_provider, callback=remove_this_code
            )

        self._pipeline.run_op(op)

    def connect(self, callback=None):
        """
        Connect to the service.

        :param callback: callback which is called when the connection to the service is complete.
        """
        logger.info("connect called")

        def pipeline_callback(call):
            if call.error:
                # TODO we need error semantics on the client
                exit(1)
            if callback:
                callback()

        self._pipeline.run_op(pipeline_ops_base.ConnectOperation(callback=pipeline_callback))

    def disconnect(self, callback=None):
        """
        Disconnect from the service.

        :param callback: callback which is called when the connection to the service has been disconnected
        """
        logger.info("disconnect called")

        def pipeline_callback(call):
            if call.error:
                # TODO we need error semantics on the client
                exit(1)
            if callback:
                callback()

        self._pipeline.run_op(pipeline_ops_base.DisconnectOperation(callback=pipeline_callback))

    def send_d2c_message(self, message, callback=None):
        """
        Send a telemetry message to the service.

        :param callback: callback which is called when the message publish has been acknowledged by the service.
        """

        def pipeline_callback(call):
            if call.error:
                # TODO we need error semantics on the client
                exit(1)
            if callback:
                callback()

        self._pipeline.run_op(
            pipeline_ops_iothub.SendD2CMessageOperation(message=message, callback=pipeline_callback)
        )

    def send_output_event(self, message, callback=None):
        """
        Send an output message to the service.

        :param callback: callback which is called when the message publish has been acknowledged by the service.
        """

        def pipeline_callback(call):
            if call.error:
                # TODO we need error semantics on the client
                exit(1)
            if callback:
                callback()

        self._pipeline.run_op(
            pipeline_ops_iothub.SendOutputEventOperation(
                message=message, callback=pipeline_callback
            )
        )

    def send_method_response(self, method_response, callback=None):
        logger.info("IoTHubPipeline send_method_response called")

        def pipeline_callback(call):
            if call.error:
                # TODO we need error semantics on the client
                exit(1)
            if callback:
                callback()

        self._pipeline.run_op(
            pipeline_ops_iothub.SendMethodResponseOperation(
                method_response=method_response, callback=pipeline_callback
            )
        )

    def enable_feature(self, feature_name, callback=None):
        """
        Enable the given feature by subscribing to the appropriate topics.

        :param feature_name: one of the feature name constants from constant.py
        :param callback: callback which is called when the feature is enabled
        """
        logger.info("enable_feature {} called".format(feature_name))
        self.feature_enabled[feature_name] = True

        def pipeline_callback(call):
            if call.error:
                # TODO we need error semantics on the client
                exit(1)
            if callback:
                callback()

        self._pipeline.run_op(
            pipeline_ops_base.EnableFeatureOperation(
                feature_name=feature_name, callback=pipeline_callback
            )
        )

    def get_twin(self, callback):
        def pipeline_callback(call):
            if call.error:
                exit(1)
            if callback:
                callback(call.twin)

        self._pipeline.run_op(pipeline_ops_iothub.GetTwinOperation(callback=pipeline_callback))

    def patch_twin_reported_properties(self, patch, callback):
        def pipeline_callback(call):
            if call.error:
                exit(1)
            if callback:
                callback()

        self._pipeline.run_op(
            pipeline_ops_iothub.PatchTwinReportedPropertiesOperation(
                patch=patch, callback=pipeline_callback
            )
        )

    def disable_feature(self, feature_name, callback=None):
        """
        Disable the given feature by subscribing to the appropriate topics.
        :param callback: callback which is called when the feature is disabled

        :param feature_name: one of the feature name constants from constant.py
        """
        logger.info("disable_feature {} called".format(feature_name))
        self.feature_enabled[feature_name] = False

        def pipeline_callback(call):
            if call.error:
                # TODO we need error semantics on the client
                exit(1)
            if callback:
                callback()

        self._pipeline.run_op(
            pipeline_ops_base.DisableFeatureOperation(
                feature_name=feature_name, callback=pipeline_callback
            )
        )
