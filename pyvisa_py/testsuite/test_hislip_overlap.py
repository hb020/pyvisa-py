"""Tests for HiSLIP synchronized and overlapped protocol state."""

import select
import socket
import struct
import threading
from unittest.mock import MagicMock

import pytest

from pyvisa_py.protocols.hislip import (
    HEADER_FORMAT,
    MESSAGETYPE,
    NO_MESSAGE_ID,
    AsyncChannel,
    AsyncMessage,
    CancellableSocket,
    InitializeResponse,
    Instrument,
    receive_exact,
)


@pytest.mark.parametrize(
    ("control_code", "expected"),
    ((0x00, False), (0x01, True), (0x02, False), (0x03, True)),
)
def test_initialize_response_uses_overlap_feature_bit(control_code, expected):
    server, client = socket.socketpair()
    try:
        server.sendall(
            struct.pack(
                HEADER_FORMAT,
                b"HS",
                MESSAGETYPE["InitializeResponse"],
                control_code,
                0x0100_0042,
                0,
            )
        )

        assert InitializeResponse(client).overlap is expected
    finally:
        client.close()
        server.close()


@pytest.mark.parametrize(
    ("overlap_enabled", "last_sent", "last_delivered", "expected"),
    (
        (False, 0x100, 0x200, 0x100),
        (True, 0x100, 0x200, 0x200),
        (False, NO_MESSAGE_ID, NO_MESSAGE_ID, NO_MESSAGE_ID),
        (True, NO_MESSAGE_ID, NO_MESSAGE_ID, NO_MESSAGE_ID),
    ),
)
def test_status_query_uses_mode_specific_message_id(
    overlap_enabled, last_sent, last_delivered, expected
):
    instrument = object.__new__(Instrument)
    instrument._state_lock = threading.RLock()
    instrument._rmt_lock = threading.Lock()
    instrument._overlap_enabled = overlap_enabled
    instrument._last_sent_message_id = last_sent
    instrument._last_delivered_message_id = last_delivered
    instrument._rmt = 1
    instrument._async_channel = MagicMock()
    instrument._async_channel.request.return_value = AsyncMessage(
        "AsyncStatusResponse", 0x42, 0, b""
    )

    assert instrument.async_status_query() == 0x42
    request_args, request_kwargs = instrument._async_channel.request.call_args
    assert request_args[0] == "AsyncStatusQuery"
    assert request_args[2] == expected
    assert request_kwargs == {
        "expected_response": "AsyncStatusResponse",
        "send_lock": instrument._rmt_lock,
    }
    with instrument._rmt_lock:
        assert request_args[1]() == 1
    assert instrument._rmt == 0


def make_receiving_instrument(overlap_enabled, last_sent=0x100):
    server, client_raw = socket.socketpair()
    instrument = object.__new__(Instrument)
    instrument._sync = CancellableSocket(client_raw)
    instrument._io_lock = threading.RLock()
    instrument._state_lock = threading.RLock()
    instrument._state_condition = threading.Condition(instrument._state_lock)
    instrument._overlap_enabled = overlap_enabled
    instrument._sync_interrupted_waiting = False
    instrument._last_sent_message_id = last_sent
    instrument._last_delivered_message_id = NO_MESSAGE_ID
    instrument._receiving = threading.Event()
    instrument._msg_type = ""
    instrument._current_message_id = NO_MESSAGE_ID
    instrument._payload_remaining = 0
    instrument._rmt = 0
    instrument._pending_data = bytearray()
    instrument._last_read_rmt = False
    instrument._last_read_termchar = False
    instrument._async_interrupted = threading.Event()
    instrument._timeout = 1.0
    return server, instrument


def send_data(server, msg_type, message_id, payload):
    server.sendall(
        struct.pack(
            HEADER_FORMAT,
            b"HS",
            MESSAGETYPE[msg_type],
            0,
            message_id,
            len(payload),
        )
        + payload
    )


def test_synchronized_receive_discards_stale_response():
    server, instrument = make_receiving_instrument(False)
    try:
        send_data(server, "DataEnd", 0x0FE, b"stale")
        send_data(server, "DataEnd", 0x100, b"current")

        assert instrument.receive() == b"current"
        assert instrument._last_delivered_message_id == 0x100
    finally:
        instrument._sync.close()
        server.close()


def test_synchronized_receive_discards_wildcard_dataend():
    server, instrument = make_receiving_instrument(False)
    try:
        send_data(server, "DataEnd", 0xFFFF_FFFF, b"stale")
        send_data(server, "DataEnd", 0x100, b"current")

        assert instrument.receive() == b"current"
        assert instrument._last_delivered_message_id == 0x100
    finally:
        instrument._sync.close()
        server.close()


def test_overlap_receive_accepts_independent_ids_after_full_delivery():
    server, instrument = make_receiving_instrument(True)
    try:
        send_data(server, "Data", 0x200, b"abc")
        send_data(server, "DataEnd", 0x202, b"def")

        assert instrument.receive(2) == b"ab"
        assert instrument._last_delivered_message_id == NO_MESSAGE_ID

        assert instrument.receive(2) == b"cd"
        assert instrument._last_delivered_message_id == 0x200

        assert instrument.receive() == b"ef"
        assert instrument._last_delivered_message_id == 0x202
        assert instrument._last_read_rmt is True
    finally:
        instrument._sync.close()
        server.close()


@pytest.mark.parametrize(
    ("initial_mode", "requested_mode", "server_features", "final_features"),
    (
        (False, True, 0b1010, 0b1011),
        (True, False, 0b1011, 0b1010),
        (False, True, 0b1010, 0b1010),
    ),
)
def test_mode_change_negotiates_only_overlap_feature_bit(
    initial_mode, requested_mode, server_features, final_features
):
    instrument = object.__new__(Instrument)
    instrument._io_lock = threading.RLock()
    instrument._state_lock = threading.RLock()
    instrument._overlap_enabled = initial_mode
    instrument._message_id = 0x100
    instrument._last_sent_message_id = 0x100
    instrument._last_delivered_message_id = 0x200
    instrument._rmt = 1
    instrument._msg_type = "Data"
    instrument._current_message_id = 0x200
    instrument._payload_remaining = 1
    instrument._pending_data = bytearray(b"x")
    instrument._last_read_rmt = True
    instrument._last_read_termchar = True
    instrument._async_interrupted = threading.Event()
    instrument.async_device_clear = MagicMock(return_value=server_features)
    instrument.device_clear_complete = MagicMock(return_value=final_features)

    accepted = instrument.set_overlap_enabled(requested_mode)

    expected_features = (server_features & ~1) | int(requested_mode)
    instrument.device_clear_complete.assert_called_once_with(expected_features)
    assert accepted is (bool(final_features & 1) == requested_mode)
    assert instrument.overlap_enabled is bool(final_features & 1)
    assert instrument._last_sent_message_id == NO_MESSAGE_ID
    assert instrument._last_delivered_message_id == NO_MESSAGE_ID


def test_setting_current_overlap_mode_does_not_clear():
    instrument = object.__new__(Instrument)
    instrument._overlap_enabled = True
    instrument.device_clear = MagicMock()

    assert instrument.set_overlap_enabled(True) is True
    instrument.device_clear.assert_not_called()


def test_synchronized_receive_discards_until_interrupted_after_async_first():
    server, instrument = make_receiving_instrument(False)
    instrument._async_interrupted.set()
    try:
        send_data(server, "DataEnd", 0x100, b"discarded")
        server.sendall(
            struct.pack(
                HEADER_FORMAT,
                b"HS",
                MESSAGETYPE["Interrupted"],
                0,
                0x100,
                0,
            )
        )
        send_data(server, "DataEnd", 0x100, b"current")

        assert instrument.receive() == b"current"
        assert instrument._async_interrupted.is_set() is False
    finally:
        instrument._sync.close()
        server.close()


def test_synchronized_receive_waits_for_async_after_interrupted_first():
    server, instrument = make_receiving_instrument(False)
    try:
        server.sendall(
            struct.pack(
                HEADER_FORMAT,
                b"HS",
                MESSAGETYPE["Interrupted"],
                0,
                0x100,
                0,
            )
        )
        send_data(server, "DataEnd", 0x100, b"current")

        timer = threading.Timer(0.05, instrument._async_interrupted.set)
        timer.start()
        assert instrument.receive() == b"current"
        timer.join()
        assert instrument._async_interrupted.is_set() is False
    finally:
        instrument._sync.close()
        server.close()


def test_synchronized_async_request_waits_for_async_interrupted():
    server, client = socket.socketpair()
    instrument = object.__new__(Instrument)
    instrument._state_lock = threading.RLock()
    instrument._state_condition = threading.Condition(instrument._state_lock)
    instrument._overlap_enabled = False
    instrument._sync_interrupted_waiting = True
    instrument._async_interrupted = threading.Event()
    instrument._async_interrupted_message_id = NO_MESSAGE_ID
    instrument._interrupt_callback = None
    instrument._timeout = 1.0
    guard_called = threading.Event()

    def request_guard():
        guard_called.set()
        instrument._ensure_async_request_allowed()

    channel = AsyncChannel(
        client,
        interrupt_callback=instrument._handle_async_interrupted,
        request_guard=request_guard,
    )
    results = []

    def send_status_query():
        try:
            results.append(
                channel.request(
                    "AsyncStatusQuery",
                    0,
                    0x100,
                    expected_response="AsyncStatusResponse",
                )
            )
        except Exception as error:
            results.append(error)

    request_thread = threading.Thread(
        target=send_status_query
    )
    request_thread.start()

    try:
        assert guard_called.wait(1.0)
        assert not select.select([server], [], [], 0.05)[0]

        server.sendall(
            struct.pack(
                HEADER_FORMAT,
                b"HS",
                MESSAGETYPE["AsyncInterrupted"],
                0,
                0x100,
                0,
            )
        )
        assert instrument._async_interrupted.wait(1.0)
        request_header = receive_exact(server, struct.calcsize(HEADER_FORMAT))
        _, msg_type, _, _, payload_length = struct.unpack(HEADER_FORMAT, request_header)
        assert msg_type == MESSAGETYPE["AsyncStatusQuery"]
        assert payload_length == 0

        server.sendall(
            struct.pack(
                HEADER_FORMAT,
                b"HS",
                MESSAGETYPE["AsyncStatusResponse"],
                0x42,
                0,
                0,
            )
        )
        request_thread.join(timeout=1.0)
        assert not request_thread.is_alive()
        assert results == [AsyncMessage("AsyncStatusResponse", 0x42, 0, b"")]
    finally:
        channel.close()
        server.close()


def test_trigger_message_id_wraps_by_two():
    instrument = object.__new__(Instrument)
    instrument._io_lock = threading.RLock()
    instrument._sync = MagicMock()
    instrument._overlap_enabled = True
    instrument._message_id = 0xFFFF_FFFE
    instrument._last_sent_message_id = NO_MESSAGE_ID
    instrument._rmt = 0

    instrument.trigger()

    header = instrument._sync.sendall.call_args.args[0]
    _, msg_type, _, message_id, _ = struct.unpack(HEADER_FORMAT, header)
    assert msg_type == MESSAGETYPE["Trigger"]
    assert message_id == 0xFFFF_FFFE
    assert instrument._message_id == 0


def test_control_requests_use_reset_message_id():
    instrument = object.__new__(Instrument)
    instrument._last_sent_message_id = NO_MESSAGE_ID
    instrument._async_channel = MagicMock()
    instrument._async_channel.request.return_value = AsyncMessage(
        "AsyncLockResponse", 1, 0, b""
    )

    assert instrument.async_lock_release() == "success"
    instrument._async_channel.request.assert_called_once_with(
        "AsyncLock",
        0,
        NO_MESSAGE_ID,
        expected_response="AsyncLockResponse",
    )

    instrument._async_channel.reset_mock()
    instrument._async_channel.request.return_value = AsyncMessage(
        "AsyncRemoteLocalResponse", 0, 0, b""
    )
    instrument.async_remote_local_control("enableRemote")
    instrument._async_channel.request.assert_called_once_with(
        "AsyncRemoteLocalControl",
        1,
        NO_MESSAGE_ID,
        expected_response="AsyncRemoteLocalResponse",
    )
