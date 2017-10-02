from demoparser.bitbuffer import Bitbuffer
import struct

from demoparser.structures import DemoHeader
from demoparser.structures import CommandHeader


class DemoFile:
    def __init__(self, demofile):
        self.data = open(demofile, 'rb')
        self.header = DemoHeader.from_data(self.data.read(1072))

    def read_command_header(self):
        return CommandHeader.from_data(self.data.read(6))

    def read_command_data(self):
        # This data fits the structure described in
        # structures.py:CommandInfo. This data seems to always
        # be all 0s though.
        self.data.read(152)

    def read_sequence_data(self):
        return struct.unpack("<ii", self.data.read(8))

    def read_user_command(self):
        seq = struct.unpack("<i", self.data.read(4))[0]
        length, buf = self.read_raw_data()

        return seq

    def read_packet_data(self):
        length = struct.unpack("<i", self.data.read(4))[0]

        index = 0
        while index < length:
            cmd = self.read_varint()
            size = self.read_varint()
            data = self.data.read(size)
            index = index + size + \
                self._varint_size(cmd) + self._varint_size(size)

            yield cmd, size, data

    def read_raw_data(self):
        length = struct.unpack("<i", self.data.read(4))[0]
        buf = self.data.read(length)

        return length, buf

    def read_bitstream(self):
        length, buf = self.read_raw_data()
        return Bitbuffer(buf)

    def read_var_bytes(self):
        length = self.read_varint()

        return self.data.read(length)

    def read_string(self):
        output = []
        while True:
            char = struct.unpack("B", self.data.read(1))[0]
            if char == 0:
                break

            output.append(chr(char))

        return "".join(output)

    def read_varint(self):
        b = 0
        count = 0
        result = 0

        cont = True
        while cont:
            data = self.data.read(1)
            b = struct.unpack("B", data)
            b = b[0]
            if count < 5:
                result |= (b & 0x7F) << (7 * count)
            count += 1
            cont = b & 0x80
        return result

    def read_short(self):
        return struct.unpack("H", self.data.read(2))[0]

    def _varint_size(self, value):
        if (value < 1 << 7):
            return 1
        elif (value < 1 << 14):
            return 2
        elif (value < 1 << 21):
            return 3
        elif (value < 1 << 28):
            return 4
        else:
            return 5
