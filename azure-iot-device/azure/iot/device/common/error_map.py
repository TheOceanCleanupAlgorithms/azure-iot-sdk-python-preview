# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from . import errors

status_code_to_error = {
    400: errors.ArgumentError,
    401: errors.UnauthorizedError,
    403: errors.QuotaExceededError,
    404: errors.NotFoundError,
    408: errors.DeviceTimeoutError,
    409: errors.DeviceAlreadyExistsError,
    412: errors.InvalidEtagError,
    413: errors.MessageTooLargeError,
    429: errors.ThrottlingError,
    500: errors.InternalServiceError,
    502: errors.BadDeviceResponseError,
    503: errors.ServiceUnavailableError,
    504: errors.TimeoutError,
}


def error_from_status_code(status_code, message=None):
    """
    Return an Error object from a failed status code

    :param int status_code: Status code returned from failed operation
    :returns: Error object
    """
    if status_code in status_code_to_error:
        return status_code_to_error[status_code](message)
    else:
        return errors.FailedStatusCodeError(message)
