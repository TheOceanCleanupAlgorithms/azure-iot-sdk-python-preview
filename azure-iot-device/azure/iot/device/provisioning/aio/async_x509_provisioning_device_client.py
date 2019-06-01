# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""This module contains user-facing asynchronous clients for the
Azure Provisioning Device SDK for Python.
"""

import logging
from azure.iot.device.common import async_adapter
from ..abstract_provisioning_device_client import AbstractProvisioningDeviceClient
from ..abstract_provisioning_device_client import log_on_register_complete
from ..internal.polling_machine import PollingMachine

logger = logging.getLogger(__name__)


class X509ProvisioningDeviceClient(AbstractProvisioningDeviceClient):
    """
    Client which can be used to run the registration of a device with provisioning service
    using X509 Certificate authentication.
    """

    def __init__(self, provisioning_pipeline):
        """
        Initializer for the X509 Provisioning Client.
        NOTE : This initializer should not be called directly.
        Instead, the class method `create_from_security_client` should be used to create a client object.
        :param provisioning_pipeline: The protocol pipeline for provisioning. As of now this only supports MQTT.
        """
        super(X509ProvisioningDeviceClient, self).__init__(provisioning_pipeline)
        self._polling_machine = PollingMachine(provisioning_pipeline)

    async def register(self):
        """
        Register the device with the provisioning service.
        Before returning the client will also disconnect from the Hub.
        If a registration attempt is made while a previous registration is in progress it may throw an error.
        """
        logger.info("Registering with Hub...")
        send_event_async = async_adapter.emulate_async(self._polling_machine.register)

        def sync_on_register_complete(result=None, error=None):
            log_on_register_complete(result, error)

        callback = async_adapter.AwaitableCallback(sync_on_register_complete)

        await send_event_async(callback=callback)
        await callback.completion()

    async def cancel(self):
        """
        Before returning the client will also disconnect from the Hub.

        In case there is no registration in process it will throw an error as there is
        no registration process to cancel.
        """
        logger.info("Disconnecting from Hub...")
        disconnect_async = async_adapter.emulate_async(self._pipeline.disconnect)

        def sync_on_cancel_complete():
            logger.info("Successfully cancelled the current registration process")

        callback = async_adapter.AwaitableCallback(sync_on_cancel_complete)

        await disconnect_async(callback=callback)
        await callback.completion()
