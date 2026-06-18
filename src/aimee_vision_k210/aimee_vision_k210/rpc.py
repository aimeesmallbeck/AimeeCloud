# This file is part of the OpenMV project.
#
# Copyright (c) 2013-2020 Ibrahim Abdelkader <iabdalkader@openmv.io>
# Copyright (c) 2013-2020 Kwabena W. Agyeman <kwagyeman@openmv.io>
#
# This work is licensed under the MIT license, see the file LICENSE for details.
#
# CPython compatible version of rpc.py for Aimee Robot

import struct
import time
import serial

class rpc:
    _COMMAND_HEADER_PACKET_MAGIC = 0x1209
    _COMMAND_DATA_PACKET_MAGIC = 0xABD1
    _RESULT_HEADER_PACKET_MAGIC = 0x9021
    _RESULT_DATA_PACKET_MAGIC = 0x1DBA

    def _crc_16(self, data, size):
        crc = 0xFFFF
        for i in range(size):
            crc ^= data[i] << 8
            for j in range(8):
                crc = (crc << 1) ^ (0x1021 if crc & 0x8000 else 0)
        return crc & 0xFFFF

    def _zero(self, buff, size):
        for i in range(size):
            buff[i] = 0

    def _same(self, data, size):
        if not size:
            return False
        old = data[0]
        for i in range(1, size):
            new = data[i]
            if new != old:
                return False
            old = new
        return True

    def _hash(self, data, size):
        h = 5381
        for i in range(size):
            h = ((h << 5) + h) ^ data[i]
        return h & 0xFFFFFFFF

    def __init__(self):
        self._stream_writer_queue_depth_max = 255
        self._get_short_timeout = 1
        self._put_short_timeout = 1

    def _get_packet_pre_alloc(self, payload_len=0):
        buff = bytearray(payload_len + 4)
        return (buff, memoryview(buff)[2:-2])

    def _get_packet(self, magic_value, payload_buf_tuple, timeout):
        packet = self.get_bytes(payload_buf_tuple[0], timeout)
        if packet is not None:
            magic = packet[0] | (packet[1] << 8)
            crc = packet[-2] | (packet[-1] << 8)
            if magic == magic_value and crc == self._crc_16(packet, len(packet) - 2):
                return payload_buf_tuple[1]
        return None

    def _set_packet(self, magic_value, payload=bytes()):
        new_payload = bytearray(len(payload) + 4)
        new_payload[:2] = struct.pack("<H", magic_value)
        new_payload[2:-2] = payload
        new_payload[-2:] = struct.pack("<H", self._crc_16(new_payload, len(payload) + 2))
        return new_payload

    def _flush(self):
        pass

    def get_bytes(self, buff, timeout_ms):
        return bytes()

    def put_bytes(self, data, timeout_ms):
        pass

class rpc_master(rpc):
    def __init__(self):
        rpc.__init__(self)

    def call(self, name, data=bytes(), send_timeout_ms=1000, recv_timeout_ms=1000):
        self._flush()
        name_data = name.encode()
        name_len = len(name_data)
        if name_len > 255: return None
        data_len = len(data)
        if data_len > 4294967295: return None
        
        # Command header
        packet = self._set_packet(self._COMMAND_HEADER_PACKET_MAGIC, struct.pack("<BI", name_len, data_len))
        self.put_bytes(packet, send_timeout_ms)
        
        # Command data
        packet = self._set_packet(self._COMMAND_DATA_PACKET_MAGIC, name_data + data)
        self.put_bytes(packet, send_timeout_ms)
        
        # Result header
        buff, view = self._get_packet_pre_alloc(4)
        res = self._get_packet(self._RESULT_HEADER_PACKET_MAGIC, (buff, view), recv_timeout_ms)
        if res is not None:
            res_len = struct.unpack("<I", res)[0]
            # Result data
            buff, view = self._get_packet_pre_alloc(res_len)
            return self._get_packet(self._RESULT_DATA_PACKET_MAGIC, (buff, view), recv_timeout_ms)
        return None

class rpc_uart_master(rpc_master):
    def __init__(self, port, baudrate=115200):
        self.__ser = serial.Serial(port, baudrate, timeout=0.1)
        rpc_master.__init__(self)

    def _flush(self):
        self.__ser.reset_input_buffer()

    def get_bytes(self, buff, timeout_ms):
        start = time.time()
        read_len = 0
        while read_len < len(buff):
            chunk = self.__ser.read(len(buff) - read_len)
            if chunk:
                buff[read_len : read_len + len(chunk)] = chunk
                read_len += len(chunk)
            if (time.time() - start) * 1000 > timeout_ms:
                return None
        return buff

    def put_bytes(self, data, timeout_ms):
        self.__ser.write(data)

    def close(self):
        self.__ser.close()

# Slave implementation omitted for brevity as it's not needed for the host node
