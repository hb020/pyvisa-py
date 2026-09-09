# -*- coding: utf-8 -*-
"""Unit tests for TCPIPInstrVxi11.gpib_command()."""

from __future__ import annotations

from unittest.mock import MagicMock

from pyvisa.constants import ResourceAttribute, StatusCode
from pyvisa_py.tcpip import TCPIPInstrVxi11


class TestTCPIPInstrVxi11DoCMD:
    def _make_session(self) -> TCPIPInstrVxi11:
        sess = object.__new__(TCPIPInstrVxi11)
        sess.interface = MagicMock()
        sess.link = 1
        sess.max_recv_size = 1024
        sess._io_timeout = 5000
        sess.timeout = 5
        sess.attrs = {
            ResourceAttribute.lockwait: 0,  # type: ignore[attr-defined]
        }
        return sess

    def test_gpib_command_maximum_size(self) -> None:
        sess = self._make_session()
        data = bytes(range(256)) * 4  # 1024 bytes
        sess.interface.device_docmd.return_value = (0, b"")

        _len , status = sess.gpib_command(data)

        assert status == StatusCode.error_invalid_parameter

    def test_gpib_command_four_bytes(self) -> None:
        sess = self._make_session()
        data = b"\x01\x02\x03\x04"
        sess.interface.device_docmd.return_value = (0, b"")

        len, status = sess.gpib_command(data)

        assert status == StatusCode.success
        assert len == 4
