# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


class OperationCancelledError(Exception):
    """
    Operation was cancelled.
    """

    pass


class ConnectionFailedError(Exception):
    """
    Connection failed to be established
    """

    pass


class ConnectionDroppedError(Exception):
    """
    Previously established connection was dropped
    """

    pass


class ArgumentError(Exception):
    """
    Service returned 400
    """

    pass


class UnauthorizedError(Exception):
    """
    Authorization failed or service returned 401
    """

    pass


class QuotaExceededError(Exception):
    """
    Service returned 403
    """

    pass


class NotFoundError(Exception):
    """
    Service returned 404
    """

    pass


class DeviceTimeoutError(Exception):
    """
    Service returned 408
    """

    # TODO: is this a method call error?  If so, do we retry?
    pass


class DeviceAlreadyExistsError(Exception):
    """
    Service returned 409
    """

    pass


class InvalidEtagError(Exception):
    """
    Service returned 412
    """

    pass


class MessageTooLargeError(Exception):
    """
    Service returned 413
    """

    pass


class ThrottlingError(Exception):
    """
    Service returned 429
    """

    pass


class InternalServiceError(Exception):
    """
    Service returned 500
    """

    pass


class BadDeviceResponseError(Exception):
    """
    Service returned 502
    """

    # TODO: is this a method invoke thing?
    pass


class ServiceUnavailableError(Exception):
    """
    Service returned 503
    """

    pass


class TimeoutError(Exception):
    """
    Operation timed out or service returned 504
    """

    pass


class FailedStatusCodeError(Exception):
    """
    Service returned unknown status code
    """

    pass


class TransportError(Exception):
    """
    Error returned from protocol client library
    """

    pass
