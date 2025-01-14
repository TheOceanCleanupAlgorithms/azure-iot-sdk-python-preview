# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
This module provides an abstract interface representing clients which can communicate with the
Device Provisioning Service.
"""

import abc
import six
import logging
from .security.sk_security_client import SymmetricKeySecurityClient
from .security.x509_security_client import X509SecurityClient
from azure.iot.device.provisioning.pipeline.provisioning_pipeline import ProvisioningPipeline

logger = logging.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class AbstractProvisioningDeviceClient(object):
    """
    Super class for any client that can be used to register devices to Device Provisioning Service.
    """

    def __init__(self, provisioning_pipeline):
        """
        Initializes the provisioning client.
        :param provisioning_pipeline: Instance of the provisioning pipeline object.
        """
        self._provisioning_pipeline = provisioning_pipeline

    @classmethod
    def create_from_symmetric_key(
        cls, provisioning_host, registration_id, id_scope, symmetric_key, protocol_choice=None
    ):
        """
        Create a client which can be used to run the registration of a device with provisioning service
        using Symmetric Key authentication.
        :param provisioning_host: Host running the Device Provisioning Service. Can be found in the Azure portal in the
        Overview tab as the string Global device endpoint
        :param registration_id: The registration ID is used to uniquely identify a device in the Device Provisioning Service.
        The registration ID is alphanumeric, lowercase string and may contain hyphens.
        :param id_scope: The ID scope is used to uniquely identify the specific provisioning service the device will
        register through. The ID scope is assigned to a Device Provisioning Service when it is created by the user and
        is generated by the service and is immutable, guaranteeing uniqueness.
        :param symmetric_key: The key which will be used to create the shared access signature token to authenticate
        the device with the Device Provisioning Service. By default, the Device Provisioning Service creates
        new symmetric keys with a default length of 32 bytes when new enrollments are saved with the Auto-generate keys
        option enabled. Users can provide their own symmetric keys for enrollments by disabling this option within
        16 bytes and 64 bytes and in valid Base64 format.
        :param protocol_choice: The choice for the protocol to be used. This is optional and will default to protocol MQTT currently.
        :return: A ProvisioningDeviceClient which can register via Symmetric Key.
        """
        if protocol_choice is not None:
            protocol_name = protocol_choice.lower()
        else:
            protocol_name = "mqtt"
        if protocol_name == "mqtt":
            security_client = SymmetricKeySecurityClient(
                provisioning_host, registration_id, id_scope, symmetric_key
            )
            mqtt_provisioning_pipeline = ProvisioningPipeline(security_client)
            return cls(mqtt_provisioning_pipeline)
        else:
            raise NotImplementedError(
                "A symmetric key can only create symmetric key security client which is compatible "
                "only with MQTT protocol.Any other protocol has not been implemented."
            )

    @classmethod
    def create_from_x509_certificate(
        cls, provisioning_host, registration_id, id_scope, x509, protocol_choice=None
    ):
        """
        Create a client which can be used to run the registration of a device with provisioning service
        using X509 certificate authentication.
        :param provisioning_host: Host running the Device Provisioning Service. Can be found in the Azure portal in the
        Overview tab as the string Global device endpoint
        :param registration_id: The registration ID is used to uniquely identify a device in the Device Provisioning Service.
        The registration ID is alphanumeric, lowercase string and may contain hyphens.
        :param id_scope: The ID scope is used to uniquely identify the specific provisioning service the device will
        register through. The ID scope is assigned to a Device Provisioning Service when it is created by the user and
        is generated by the service and is immutable, guaranteeing uniqueness.
        :param x509: The x509 certificate, To use the certificate the enrollment object needs to contain cert (either the root certificate or one of the intermediate CA certificates).
        If the cert comes from a CER file, it needs to be base64 encoded.
        :param protocol_choice: The choice for the protocol to be used. This is optional and will default to protocol MQTT currently.
        :return: A ProvisioningDeviceClient which can register via Symmetric Key.
        """
        if protocol_choice is None:
            protocol_name = "mqtt"
        else:
            protocol_name = protocol_choice.lower()
        if protocol_name == "mqtt":
            security_client = X509SecurityClient(provisioning_host, registration_id, id_scope, x509)
            mqtt_provisioning_pipeline = ProvisioningPipeline(security_client)
            return cls(mqtt_provisioning_pipeline)
        else:
            raise NotImplementedError(
                "A x509 certificate can only create x509 security client which is compatible only "
                "with MQTT protocol.Any other protocol has not been implemented."
            )

    @abc.abstractmethod
    def register(self):
        """
        Register the device with the Device Provisioning Service.
        """
        pass

    @abc.abstractmethod
    def cancel(self):
        """
        Cancel an in progress registration of the device with the Device Provisioning Service.
        """
        pass


def log_on_register_complete(result=None, error=None):
    # This could be a failed/successful registration result from DPS
    # or a error from polling machine. Response should be given appropriately
    if result is not None:
        if result.status == "assigned":
            logger.info("Successfully registered with Provisioning Service")
        else:  # There be other statuses
            logger.error("Failed registering with Provisioning Service")
    if error is not None:  # This can only happen when the polling machine runs into error
        logger.info(error)
