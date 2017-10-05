from demoparser.bitbuffer import Bitbuffer
import struct

from demoparser.structures import CommandHeader


class Bytebuffer:
    r"""
    Parse a stream of bytes from a .DEM file.

    This class provdes convenience methods for parsing
    .DEM files. It handles unpacking bytes to different
    data types, reading variable-length integers, reading
    strings, and creating Bitbuffers.

    :Example:

    >>> b = Bytebuffer(b'\x00\xf1\xaa')
    >>> b.read(1)
    0
    >>> b.read_short()
    43761
    """

    def __init__(self, data):
        self.data = data
        self.index = 0

    def read(self, num_bytes):
        """Read `num_bytes` bytes from buffer."""
        d = self.data[self.index:self.index + num_bytes]
        self.index += num_bytes
        return d

    def read_command_header(self):
        """Read the 6 byte command header.

        See :ref:`CommandHeader description <header-format>`
        for more details.

        :returns: CommandHeader instance
        """
        return CommandHeader.from_data(self.read(6))

    def read_command_data(self):
        """Read command info structure.

        This is not used by the parser.

        :returns: bytes
        """
        # This data fits the structure described in
        # structures.py:CommandInfo. This data seems to always
        # be all 0s though. It doesn't appear to be very useful
        # and it is very expensive to create one of these structures
        # for each message.
        self.read(152)

    def read_sequence_data(self):
        """Read two integers.

        This data is not used by the parser.

        :returns: Tuple of integers
        """
        return struct.unpack("<ii", self.read(8))

    def read_user_command(self):
        """Read a user command."""
        seq = struct.unpack("<i", self.read(4))[0]
        length, buf = self.read_raw_data()

        return seq

    def read_packet_data(self):
        """Read a demo packet.

        Each packet consists of a command and data.
        The command is an ID that references either a NET\_ or
        SVC\_ class defined in netmessages.proto.

        The data is used to instantiate the class referred to
        by command.

        :returns: Tuple (command, data)
        """
        length = struct.unpack("<i", self.read(4))[0]

        index = 0
        while index < length:
            cmd = self.read_varint()
            size = self.read_varint()
            data = self.read(size)
            index = index + size + \
                self._varint_size(cmd) + self._varint_size(size)

            yield cmd, size, data

    def read_raw_data(self):
        """Read number of bytes specified by a signed int.

        First a 32-bit signed integer is read, then
        that number of bytes is read from the stream.

        :returns: Tuple (bytes_read, bytes)
        """
        length = struct.unpack("<i", self.read(4))[0]
        buf = self.read(length)

        return length, buf

    def read_bitstream(self):
        """Create a Bitbuffer from a number of bytes.

        The numbers of bytes to include in the Bitbuffer is
        read. Then that number of bytes is used to instantiate
        a Bitbuffer instance.

        :returns: Bitbuffer instance
        """
        length, buf = self.read_raw_data()
        return Bitbuffer(buf)

    def read_var_bytes(self):
        """Read number of bytes specified by a varint.

        First a varint is read and then the number
        of bytes specified by the varint are read.

        :returns: bytestring
        """
        length = self.read_varint()
        return self.read(length)

    def read_string(self):
        r"""Read a zero-terminated string.

        Reads characters until \\0 is encountered.

        :returns: str
        """
        output = []
        while True:
            char = struct.unpack("B", self.read(1))[0]
            if char == 0:
                break

            output.append(chr(char))

        return "".join(output)

    def read_varint(self):
        """Read a variable-length integer.

        :returns: Integer
        """
        b = 0
        count = 0
        result = 0

        cont = True
        while cont:
            data = self.read(1)
            b = struct.unpack("B", data)
            b = b[0]
            if count < 5:
                result |= (b & 0x7F) << (7 * count)
            count += 1
            cont = b & 0x80
        return result

    def read_short(self):
        """Read a 16-bit unsigned short."""
        return struct.unpack("H", self.read(2))[0]

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
