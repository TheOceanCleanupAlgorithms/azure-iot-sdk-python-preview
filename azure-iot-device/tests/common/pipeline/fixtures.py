# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import pytest
import threading
from tests.common.pipeline import helpers
from azure.iot.device.common import unhandled_exceptions
from azure.iot.device.common.pipeline import (
    pipeline_events_base,
    pipeline_ops_base,
    pipeline_thread,
)


@pytest.fixture
def callback(mocker):
    return mocker.Mock()


@pytest.fixture
def fake_exception():
    return Exception()


@pytest.fixture
def fake_base_exception():
    return helpers.UnhandledException()


class FakeEvent(pipeline_events_base.PipelineEvent):
    def __init__(self):
        super(FakeEvent, self).__init__()


@pytest.fixture
def event():
    return FakeEvent()


class FakeOperation(pipeline_ops_base.PipelineOperation):
    def __init__(self, callback=None):
        super(FakeOperation, self).__init__(callback=callback)


@pytest.fixture
def op(callback):
    op = FakeOperation(callback=callback)
    op.name = "op"
    return op


@pytest.fixture
def op2(callback):
    op = FakeOperation(callback=callback)
    op.name = "op2"
    return op


@pytest.fixture
def op3(callback):
    op = FakeOperation(callback=callback)
    op.name = "op3"
    return op


@pytest.fixture
def finally_op(callback):
    op = FakeOperation(callback=callback)
    op.name = "finally_op"
    return op


@pytest.fixture
def new_op(callback):
    op = FakeOperation(callback=callback)
    op.name = "new_op"
    return op


@pytest.fixture
def fake_pipeline_thread():
    """
    This fixture mocks out the thread name so that the pipeline decorators
    use to assert that you are in a pipeline thread.
    """
    this_thread = threading.current_thread()
    old_name = this_thread.name

    this_thread.name = "pipeline"
    yield
    this_thread.name = old_name


@pytest.fixture
def fake_non_pipeline_thread():
    """
    This fixture sets thread name to something other than "pipeline" to force asserts
    """
    this_thread = threading.current_thread()
    old_name = this_thread.name

    this_thread.name = "not pipeline"
    yield
    this_thread.name = old_name


@pytest.fixture
def unhandled_error_handler(mocker):
    return mocker.patch.object(unhandled_exceptions, "exception_caught_in_background_thread")
