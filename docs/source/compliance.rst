VPP-4.3 standard Attribute Compliance
=====================================

This document assesses the VPP-4.3 attributes applicable to PyVISA-py's
implemented resource types: ``GPIB::INSTR``, ``GPIB::INTFC``, ``ASRL::INSTR``,
``TCPIP::INSTR`` over VXI-11 and HiSLIP, ``TCPIP::SOCKET``, and ``USB::INSTR``. 

Resource classes not listed in a section cannot use that attribute under VPP-4.3.

# TODO: add prologix

``VI_ATTR_4882_COMPLIANT``
--------------------------
Usable by USB INSTR.

Coverage: Missing.


``VI_ATTR_ASRL_AVAIL_NUM``
--------------------------
Usable by ASRL INSTR.

Coverage: Full.


``VI_ATTR_ASRL_BAUD``
---------------------
Usable by ASRL INSTR.

Coverage: Full.


``VI_ATTR_ASRL_CTS_STATE``
--------------------------
Usable by ASRL INSTR.

Coverage: Full.


``VI_ATTR_ASRL_DATA_BITS``
--------------------------
Usable by ASRL INSTR.

Coverage: Full.


``VI_ATTR_ASRL_DCD_STATE``
--------------------------
Usable by ASRL INSTR.

Coverage: Missing.


``VI_ATTR_ASRL_DSR_STATE``
--------------------------
Usable by ASRL INSTR.

Coverage: Full.


``VI_ATTR_ASRL_DTR_STATE``
--------------------------
Usable by ASRL INSTR.

Coverage: Missing.


``VI_ATTR_ASRL_END_IN``
-----------------------
Usable by ASRL INSTR.

Coverage: Full.


``VI_ATTR_ASRL_END_OUT``
------------------------
Usable by ASRL INSTR.

Coverage: Full.


``VI_ATTR_ASRL_FLOW_CNTRL``
---------------------------
Usable by ASRL INSTR.

Coverage: Full.


``VI_ATTR_ASRL_PARITY``
-----------------------
Usable by ASRL INSTR.

Coverage: Full.


``VI_ATTR_ASRL_REPLACE_CHAR``
-----------------------------
Usable by ASRL INSTR.

Coverage: Missing.


``VI_ATTR_ASRL_RI_STATE``
-------------------------
Usable by ASRL INSTR.

Coverage: Missing.


``VI_ATTR_ASRL_RTS_STATE``
--------------------------
Usable by ASRL INSTR.

Coverage: Missing.


``VI_ATTR_ASRL_STOP_BITS``
--------------------------
Usable by ASRL INSTR.

Coverage: Full.


``VI_ATTR_ASRL_XOFF_CHAR``
--------------------------
Usable by ASRL INSTR.

Coverage: Missing.


``VI_ATTR_ASRL_XON_CHAR``
-------------------------
Usable by ASRL INSTR.

Coverage: Missing.


``VI_ATTR_DEV_STATUS_BYTE``
---------------------------
Usable by GPIB INTFC.

Coverage: Missing.


``VI_ATTR_DMA_ALLOW_EN``
------------------------
Usable by all resources.

Coverage: HiSLIP Partial; all others Missing. 

HiSLIP exposes a constant disabled value instead of providing
the required writable attribute and unsupported-state response.

Proposition: add to all (`dma_allow_enabled`), in faked RO (False).


``VI_ATTR_FILE_APPEND_EN``
--------------------------
Usable by all resources.

Coverage: HiSLIP Partial; all others Missing. 

HiSLIP exposes a constant false value, but it is not writable
and is not used by file transfer operations.

Proposition: add to all (`file_append_enabled`), in faked RO (False).


``VI_ATTR_GPIB_ADDR_STATE``
---------------------------
Usable by GPIB INTFC.

Coverage: Missing.



``VI_ATTR_GPIB_ATN_STATE``
--------------------------
Usable by GPIB INTFC.

Coverage: Full.


``VI_ATTR_GPIB_CIC_STATE``
--------------------------
Usable by GPIB INTFC.

Coverage: Full.


``VI_ATTR_GPIB_HS488_CBL_LEN``
-------------------------------
Usable by GPIB INTFC.

Coverage: Missing.


``VI_ATTR_GPIB_NDAC_STATE``
---------------------------
Usable by GPIB INTFC.

Coverage: Full.


``VI_ATTR_GPIB_PRIMARY_ADDR``
-----------------------------
Usable by GPIB INSTR and GPIB INTFC.

Coverage: Full.


``VI_ATTR_GPIB_READDR_EN``
--------------------------
Usable by GPIB INSTR.

Coverage: Full.


``VI_ATTR_GPIB_REN_STATE``
--------------------------
Usable by GPIB INSTR and GPIB INTFC.

Coverage: Full.


``VI_ATTR_GPIB_SECONDARY_ADDR``
-------------------------------
Usable by GPIB INSTR and GPIB INTFC.

Coverage: Full.


``VI_ATTR_GPIB_SRQ_STATE``
--------------------------
Usable by GPIB INTFC.

Coverage: Full.


``VI_ATTR_GPIB_SYS_CNTRL_STATE``
--------------------------------
Usable by GPIB INTFC.

Coverage: Missing.


``VI_ATTR_GPIB_UNADDR_EN``
--------------------------
Usable by GPIB INSTR.

Coverage: Full.


``VI_ATTR_INTF_INST_NAME``
--------------------------
Usable by all resources.

Coverage: HiSLIP Full; all others Missing.

Proposition: add to all (`interface_instrument_name`).


``VI_ATTR_INTF_NUM``
--------------------
Usable by all resources.

Coverage: GPIB INSTR, GPIB INTFC, HiSLIP, and TCPIP SOCKET Full; 
ASRL, VXI-11, and USB Missing.

Proposition: add to all (`interface_number`)


``VI_ATTR_INTF_TYPE``
---------------------
Usable by all resources.

Coverage: Full.


``VI_ATTR_IO_PROT``
-------------------
Usable by GPIB INSTR, ASRL INSTR, TCPIP SOCKET, and USB INSTR.

Coverage: 
GPIB partial: only normal protocol is supported;
ASRL and SOCKET full: VI_PROT_4882_STRS is accepted; 
USB Missing. 

Proposition: add to all (`io_prot`)

``VI_ATTR_MANF_ID``
-------------------
Usable by USB INSTR.

Coverage: Full.


``VI_ATTR_MANF_NAME``
---------------------
Usable by USB INSTR.

Coverage: Missing.


``VI_ATTR_MAX_QUEUE_LENGTH``
----------------------------
Usable by all resources.

Coverage: Missing.


``VI_ATTR_MODEL_CODE``
----------------------
Usable by USB INSTR.

Coverage: Full.


``VI_ATTR_MODEL_NAME``
----------------------
Usable by USB INSTR.

Coverage: Missing.


``VI_ATTR_RD_BUF_OPER_MODE``
----------------------------
Usable by all resources.

Coverage: HiSLIP Partial; all others Missing. 

HiSLIP stores the default but does not provide formatted read
buffer behavior.


``VI_ATTR_RD_BUF_SIZE``
-----------------------
Usable by all resources.

Coverage: Missing.


``VI_ATTR_RM_SESSION``
----------------------
Usable by all resources.

Coverage: Full.


``VI_ATTR_RSRC_CLASS``
----------------------
Usable by all resources.

Coverage: Full.


``VI_ATTR_RSRC_IMPL_VERSION``
-----------------------------
Usable by all resources.

Coverage: Missing.


``VI_ATTR_RSRC_LOCK_STATE``
---------------------------
Usable by all resources.

Coverage: HiSLIP Partial; all others Missing. 

HiSLIP stores ``VI_NO_LOCK`` but does not implement VISA lock
acquisition, sharing, nesting, or remote lock-state reporting.

#TODO: update after #643


``VI_ATTR_RSRC_MANF_ID``
------------------------
Usable by all resources.

Coverage: Missing.


``VI_ATTR_RSRC_MANF_NAME``
--------------------------
Usable by all resources.

Coverage: Missing.


``VI_ATTR_RSRC_NAME``
---------------------
Usable by all resources. 

Coverage: Full.


``VI_ATTR_RSRC_SPEC_VERSION``
-----------------------------
Usable by all resources. 

Coverage: Missing.


``VI_ATTR_SEND_END_EN``
-----------------------
Usable by all resources.

Coverage: GPIB INSTR and GPIB
INTFC Full; ASRL, VXI-11, HiSLIP, and USB Partial; SOCKET Missing. The partial
implementations expose or read the setting but do not consistently apply it to
the underlying transport's end-of-message behavior.


``VI_ATTR_SUPPRESS_END_EN``
---------------------------
Usable by GPIB INSTR, ASRL INSTR, TCPIP INSTR (VXI-11 and HiSLIP), TCPIP
SOCKET, and USB INSTR. 

Coverage: ASRL,
VXI-11, SOCKET, and USB Full; HiSLIP Partial; GPIB Missing. HiSLIP stores the
value but its receive implementation does not honor it.


``VI_ATTR_TCPIP_ADDR``
----------------------
Usable by TCPIP INSTR (VXI-11 and HiSLIP) and TCPIP SOCKET. 

Coverage: Full.


``VI_ATTR_TCPIP_DEVICE_NAME``
-----------------------------
Usable by TCPIP INSTR (VXI-11 and HiSLIP).

Coverage: Full.


``VI_ATTR_TCPIP_HISLIP_MAX_MESSAGE_KB``
----------------------------------------
Usable by TCPIP INSTR (HiSLIP).

Coverage: Full.


``VI_ATTR_TCPIP_HISLIP_OVERLAP_EN``
------------------------------------
Usable by TCPIP INSTR (HiSLIP).

Coverage: Partial. 

The value is stored but changes do not issue the required HiSLIP device clear or switch the
protocol's overlap mode.


``VI_ATTR_TCPIP_HISLIP_VERSION``
---------------------------------
Usable by TCPIP INSTR (HiSLIP).

Coverage: Full.


``VI_ATTR_TCPIP_HOSTNAME``
--------------------------
Usable by TCPIP INSTR (VXI-11 and HiSLIP) and TCPIP SOCKET. 

Coverage: Full.


``VI_ATTR_TCPIP_IS_HISLIP``
---------------------------
Usable by TCPIP INSTR (VXI-11 and HiSLIP).

Coverage: Full.


``VI_ATTR_TCPIP_KEEPALIVE``
---------------------------
Usable by TCPIP INSTR (HiSLIP) and TCPIP SOCKET.

Coverage: Full.


``VI_ATTR_TCPIP_NODELAY``
-------------------------
Usable by TCPIP INSTR (HiSLIP) and TCPIP SOCKET.

Coverage:
SOCKET Full; HiSLIP Partial. 

HiSLIP reports a stored value but does not set the
TCP socket's ``TCP_NODELAY`` option.


``VI_ATTR_TCPIP_PORT``
----------------------
Usable by TCPIP INSTR (HiSLIP) and TCPIP SOCKET.

Coverage: Full.


``VI_ATTR_TERMCHAR``
--------------------
Usable by all resources.

Coverage: all Full except
HiSLIP Partial. HiSLIP stores the value but does not use it to terminate reads.


``VI_ATTR_TERMCHAR_EN``
-----------------------
Usable by all resources.

Coverage: all Full except
HiSLIP Partial. HiSLIP stores the value but does not use it to terminate reads.


``VI_ATTR_TMO_VALUE``
---------------------
Usable by all resources.

Coverage: Full.


``VI_ATTR_TRIG_ID``
-------------------
Usable by GPIB INSTR, ASRL INSTR, TCPIP INSTR (VXI-11 and HiSLIP), and USB
INSTR.

Coverage: Missing.


``VI_ATTR_USB_INTFC_NUM``
-------------------------
Usable by USB INSTR.

Coverage: Full.


``VI_ATTR_USB_MAX_INTR_SIZE``
------------------------------
Usable by USB INSTR.

Coverage: Missing.


``VI_ATTR_USB_PROTOCOL``
------------------------
Usable by USB INSTR.

Coverage: Missing.


``VI_ATTR_USB_SERIAL_NUM``
--------------------------
Usable by USB INSTR.

Coverage: Full.


``VI_ATTR_USER_DATA``
---------------------
Usable by all resources.

Coverage: Missing.


``VI_ATTR_WR_BUF_OPER_MODE``
----------------------------
Usable by all resources.

Coverage: HiSLIP Partial; 
All others Missing. HiSLIP stores the default but has no formatted write buffer.


``VI_ATTR_WR_BUF_SIZE``
-----------------------
Usable by all resources.

Coverage: Missing.

Additionally supported attributes
=================================

``VI_KTATTR_LOCKWAIT``
----------------------
Usable by all VXI-11 INSTR.

This is a PyVISA-Py and Keysight specific attribute.

Coverage: Full.
