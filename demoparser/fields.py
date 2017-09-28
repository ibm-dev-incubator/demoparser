import struct

from suitcase.fields import BaseField
from suitcase.fields import BaseStructField
from suitcase.fields import BaseFixedByteSequence


class SLFloat32(BaseStructField):
    """Signed Little Endian 32-bit float field"""
    PACK_FORMAT = UNPACK_FORMAT = b"<f"

    def unpack(self, data, **kwargs):
        self._value = struct.unpack(self.UNPACK_FORMAT, data)[0]


class UBInt32Sequence(BaseFixedByteSequence):
    "A sequence of unsigned, big-endian 32 bit integers"

    def __init__(self, length, **kwargs):
        super().__init__(lambda l: ">" + "I" * l, length, **kwargs)
        self.bytes_required = length * 4


class FixedLengthString(BaseField):
    """
    Reads a fixed number of bytes (interpreted as ASCII) from input stream
    """

    def __init__(self, length, **kwargs):
        super().__init__(**kwargs)
        self.length = length

    @property
    def bytes_required(self):
        "Number of bytes to read from stream"
        return self.length

    def pack(self, stream):
        stream.write(self._value.strip(b'\0'))

    def unpack(self, data):
        self._value = data.strip(b'\0')
