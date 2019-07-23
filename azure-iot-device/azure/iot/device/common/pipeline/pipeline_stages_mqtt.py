# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import logging
from . import (
    pipeline_ops_base,
    PipelineStage,
    pipeline_ops_mqtt,
    pipeline_events_mqtt,
    operation_flow,
    pipeline_thread,
)
from azure.iot.device.common.mqtt_transport import MQTTTransport
from azure.iot.device.common import unhandled_exceptions, errors

logger = logging.getLogger(__name__)


class MQTTClientStage(PipelineStage):
    """
    PipelineStage object which is responsible for interfacing with the MQTT protocol wrapper object.
    This stage handles all MQTT operations and any other operations (such as ConnectOperation) which
    is not in the MQTT group of operations, but can only be run at the protocol level.
    """

    @pipeline_thread.runs_on_pipeline_thread
    def _cancel_active_connect_disconnect_ops(self):
        """
        Cancel any running connect or disconnect op.  Since our ability to "cancel" is fairly limited,
        all this does (for now) is to fail the operation
        """

        ops_to_cancel = []
        if self._active_connect_op:
            # TODO: should this actually run a cancel call on the op?
            ops_to_cancel.add(self._active_connect_op)
            self._active_connect_op = None
        if self._active_disconnect_op:
            ops_to_cancel.add(self._active_disconnect_op)
            self._active_disconnect_op = None

        for op in ops_to_cancel:
            op.error = errors.PipelineError(
                "Cancelling because new ConnectOperation, DisconnectOperation, or ReconnectOperation was issued"
            )
            operation_flow.complete_op(stage=self, op=op)

    @pipeline_thread.runs_on_pipeline_thread
    def _run_op(self, op):
        if isinstance(op, pipeline_ops_mqtt.SetMQTTConnectionArgsOperation):
            # pipeline_ops_mqtt.SetMQTTConnectionArgsOperation is where we create our MQTTTransport object and set
            # all of its properties.
            logger.info("{}({}): got connection args".format(self.name, op.name))
            self.hostname = op.hostname
            self.username = op.username
            self.client_id = op.client_id
            self.ca_cert = op.ca_cert
            self.sas_token = None
            self.trusted_certificate_chain = None
            self.transport = MQTTTransport(
                client_id=self.client_id,
                hostname=self.hostname,
                username=self.username,
                ca_cert=self.ca_cert,
            )
            self.transport.on_mqtt_connected = self._handle_mqtt_connected
            self.transport.on_mqtt_connection_failure = self._handle_mqtt_connection_failure
            self.transport.on_mqtt_disconnected = self._handle_mqtt_disconnected
            self.transport.on_mqtt_message_received = self._handle_mqtt_message_received
            self._active_connect_op = None
            self._active_disconnect_op = None
            self.pipeline_root.transport = self.transport
            operation_flow.complete_op(self, op)

        elif isinstance(op, pipeline_ops_base.SetSasTokenOperation):
            # When we get a sas token from above, we just save it for later
            logger.info("{}({}): got password".format(self.name, op.name))
            self.sas_token = op.sas_token
            operation_flow.complete_op(self, op)

        elif isinstance(op, pipeline_ops_base.SetClientAuthenticationCertificateOperation):
            # When we get a certificate from above, we just save it for later
            logger.info("{}({}): got certificate".format(self.name, op.name))
            self.trusted_certificate_chain = op.certificate
            operation_flow.complete_op(self, op)

        elif isinstance(op, pipeline_ops_base.ConnectOperation):
            logger.info("{}({}): conneting".format(self.name, op.name))

            self._cancel_active_connect_disconnect_ops()
            self._active_connect_op = op
            try:
                self.transport.connect(
                    password=self.sas_token, client_certificate=self.trusted_certificate_chain
                )
            except Exception as e:
                self._active_connect_op = None
                raise e

        elif isinstance(op, pipeline_ops_base.ReconnectOperation):
            logger.info("{}({}): reconnecting".format(self.name, op.name))

            # We set _active_connect_op here because a reconnect is the same as a connect for "active operation" tracking purposes.
            self._cancel_active_connect_disconnect_ops()
            self._active_connect_op = op
            try:
                self.transport.reconnect(self.sas_token)
            except Exception as e:
                self._active_connect_op = None
                raise e

        elif isinstance(op, pipeline_ops_base.DisconnectOperation):
            logger.info("{}({}): disconnecting".format(self.name, op.name))

            self._cancel_active_connect_disconnect_ops()
            self._active_disconnect_op = op
            try:
                self.transport.disconnect()
            except Exception as e:
                self._active_disconnect_op = None
                raise e

        elif isinstance(op, pipeline_ops_mqtt.MQTTPublishOperation):
            logger.info("{}({}): publishing on {}".format(self.name, op.name, op.topic))

            @pipeline_thread.invoke_on_pipeline_thread_nowait
            def on_published():
                logger.info("{}({}): PUBACK received. completing op.".format(self.name, op.name))
                operation_flow.complete_op(self, op)

            self.transport.publish(topic=op.topic, payload=op.payload, callback=on_published)

        elif isinstance(op, pipeline_ops_mqtt.MQTTSubscribeOperation):
            logger.info("{}({}): subscribing to {}".format(self.name, op.name, op.topic))

            @pipeline_thread.invoke_on_pipeline_thread_nowait
            def on_subscribed():
                logger.info("{}({}): SUBACK received. completing op.".format(self.name, op.name))
                operation_flow.complete_op(self, op)

            self.transport.subscribe(topic=op.topic, callback=on_subscribed)

        elif isinstance(op, pipeline_ops_mqtt.MQTTUnsubscribeOperation):
            logger.info("{}({}): unsubscribing from {}".format(self.name, op.name, op.topic))

            @pipeline_thread.invoke_on_pipeline_thread_nowait
            def on_unsubscribed():
                logger.info("{}({}): UNSUBACK received.  completing op.".format(self.name, op.name))
                operation_flow.complete_op(self, op)

            self.transport.unsubscribe(topic=op.topic, callback=on_unsubscribed)

        else:
            operation_flow.pass_op_to_next_stage(self, op)

    @pipeline_thread.invoke_on_pipeline_thread_nowait
    def _handle_mqtt_message_received(self, topic, payload):
        """
        Handler that gets called by the protocol library when an incoming message arrives.
        Convert that message into a pipeline event and pass it up for someone to handle.
        """
        operation_flow.pass_event_to_previous_stage(
            stage=self,
            event=pipeline_events_mqtt.IncomingMQTTMessageEvent(topic=topic, payload=payload),
        )

    @pipeline_thread.invoke_on_pipeline_thread_nowait
    def _handle_mqtt_connected(self):
        """
        Handler that gets called by the transport when it connects.
        """
        logger.info("_handle_mqtt_connected called")
        if self._active_connect_op:
            logger.info("completing connect op")
            op = self._active_connect_op
            self._active_connect_op = None
            operation_flow.complete_op(stage=self, op=op)
        else:
            logger.warning("Connection was unexpected")
        # self.on_connected() tells other pipeilne stages that we're connected
        self.on_connected()

    @pipeline_thread.invoke_on_pipeline_thread_nowait
    def _handle_mqtt_connection_failure(self, cause):
        """
        Handler that gets called by the transport when a connection fails.
        """

        logger.error("{}: _handle_mqtt_connection_failure called: {}".format(self.name, cause))
        if self._active_connect_op:
            logger.info("{}: failing connect op".format(self.name))
            op = self._active_connect_op
            self._active_connect_op = None
            op.error = cause
            operation_flow.complete_op(stage=self, op=op)
        else:
            logger.warning("{}: Connection failure was unexpected".format(self.name))
            unhandled_exceptions.exception_caught_in_background_thread(cause)

    @pipeline_thread.invoke_on_pipeline_thread_nowait
    def _handle_mqtt_disconnected(self, cause):
        """
        Handler that gets called by the transport when the transport disconnects.
        """
        logger.error("{}: _handle_mqtt_disconnect called: {}".format(self.name, cause))
        if self._active_disconnect_op:
            logger.info("{}: completing disconnect op".format(self.name))
            op = self._active_disconnect_op
            self._active_disconnect_op = None
            op.error = cause
            operation_flow.complete_op(stage=self, op=op)
        else:
            logger.warning("{}: disconnection was unexpected".format(self.name))
            unhandled_exceptions.exception_caught_in_background_thread(cause)
        # self.on_disconnected() tells other pipeilne stages that we're disconnected
        self.on_disconnected()
