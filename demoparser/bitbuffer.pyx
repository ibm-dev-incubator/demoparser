# cython: profile=True
from cython.operator cimport dereference
from cpython cimport array
import array
from libc.math cimport ceil

from demoparser import consts


cdef unsigned int[33] mask_table = [
    0,
    ( 1 << 1 ) - 1,
    ( 1 << 2 ) - 1,
    ( 1 << 3 ) - 1,
    ( 1 << 4 ) - 1,
    ( 1 << 5 ) - 1,
    ( 1 << 6 ) - 1,
    ( 1 << 7 ) - 1,
    ( 1 << 8 ) - 1,
    ( 1 << 9 ) - 1,
    ( 1 << 10 ) - 1,
    ( 1 << 11 ) - 1,
    ( 1 << 12 ) - 1,
    ( 1 << 13 ) - 1,
    ( 1 << 14 ) - 1,
    ( 1 << 15 ) - 1,
    ( 1 << 16 ) - 1,
    ( 1 << 17 ) - 1,
    ( 1 << 18 ) - 1,
    ( 1 << 19 ) - 1,
    ( 1 << 20 ) - 1,
    ( 1 << 21 ) - 1,
    ( 1 << 22 ) - 1,
    ( 1 << 23 ) - 1,
    ( 1 << 24 ) - 1,
    ( 1 << 25 ) - 1,
    ( 1 << 26 ) - 1,
    ( 1 << 27 ) - 1,
    ( 1 << 28 ) - 1,
    ( 1 << 29 ) - 1,
    ( 1 << 30 ) - 1,
    0x7fffffff,
    0xffffffff,
]


cdef class Bitbuffer:

    def __init__(self, data, num_bytes=None, num_bits=None):
        self.num_bytes = num_bytes or len(data)
        self.num_bits = num_bits or self.num_bytes << 3

        # We have to keep a reference to the Python object around.
        # It will be garbage-collected when __init__ exits otherwise.
        # This doesn't segfault, and we can keep reading from the pointer.
        # Parsing will fail far away from here though because the data
        # being read isn't a buffer from a demo file.
        self.orig_data = data

        # Cython does not let you cast Python objects directly so
        # `<unsigned int *> data` will not work. It has to go through the
        # intermediate <char *> cast.
        self.data = <unsigned int *><char *>data

        # Length in words where 1 word = 32 bits = 4 bytes
        self.length = int(ceil(self.num_bytes/4.0))
        self.index = 0
        self.bits_avail = 32
        self.next_dword()

    cpdef unsigned int next_dword(self):
        """Move to the next 32-bit integer in the stream.

        :returns: unsigned int
        """
        if self.index == self.length:
            self.bits_avail = 1
            self.in_buf_word = 0
            self.index += 1
        else:
            if self.index > self.length:
                self.in_buf_word = 0
            else:
                self.in_buf_word = self.data[self.index]
                self.index += 1

    cpdef unsigned char read_bit(self):
        """Read a single bit.

        :returns: one bit
        """
        cdef unsigned char ret = self.in_buf_word & 1
        self.bits_avail -= 1

        if self.bits_avail == 0:
            self.bits_avail = 32
            self.next_dword()
        else:
            self.in_buf_word >>= 1

        return ret

    cpdef unsigned int read_uint_bits(self, unsigned int bits):
        """Read the unsigned integer represented by `bits` bits.

        If the number of bits remaining in the current word is
        not enough then the next word will be read.

        :param bits: Number of bits to read
        :type bits: unsigned int
        :returns: unsigned int
        """
        cdef unsigned int ret = self.in_buf_word & mask_table[bits]

        if self.bits_avail >= bits:
            ret = self.in_buf_word & mask_table[bits]

            self.bits_avail -= bits
            if self.bits_avail:
                self.in_buf_word >>= bits
            else:
                self.bits_avail = 32
                self.next_dword()

            return ret
        else:
            # Merge words
            ret = self.in_buf_word
            bits -= self.bits_avail
            self.next_dword()

            ret |= ((self.in_buf_word & mask_table[bits]) << self.bits_avail)
            self.bits_avail = 32 - bits
            self.in_buf_word >>= bits

        return ret

    cpdef int read_sint_bits(self, unsigned int bits):
        """Read a signed integer of `bits` bits.

        First an unsigned integer is read then a two's complement
        integer is computed.

        :param bits: Number of bits to read
        :type bits: unsigned int
        :returns: int
        """
        cdef unsigned int ret = self.read_uint_bits(bits)
        cdef unsigned int mask = 2 << (bits - 2)
        return -(ret & mask) + (ret & ~mask)

    cpdef unsigned int read_var_int(self):
        """Read a variable length integer.

        :returns: unsigned int
        """
        cdef unsigned int num = self.read_uint_bits(6)
        cdef unsigned char bits = num & (16 | 32)

        if bits == 16:
            num = (num & 15) | (self.read_uint_bits(4) << 4)
            assert num >= 16
        elif bits == 32:
            num = (num & 15) | (self.read_uint_bits(8) << 4)
            assert num >= 256
        elif bits == 48:
            num = (num & 15) | (self.read_uint_bits(28) << 4)
            assert num >= 4096

        return num

    cpdef str read_string(self, int length=-1):
        r"""Read a string.

        If length is not provided characters are read until
        \\0 is reached. If length is provided then exactly
        length bytes will be read and the string may not be
        zero-terminated.

        :returns: str
        """
        cdef char c
        cdef bint append = True
        cdef int index = 1
        ret = []

        while True:
            c = self.read_uint_bits(8)
            if c == 0:
                append = False
                if length == -1:
                    break

            if append:
                ret.append(c)
            if index == length:
                break

            index += 1

        return array.array('b', ret).tobytes().decode('utf-8')

    cpdef float read_bit_normal(self):
        cdef bint sign_bit = self.read_bit()
        """Read a float normal.

        :returns: float value between -1.0 and 1.0
        """
        cdef int frac = self.read_uint_bits(consts.NORMAL_FRACTIONAL_BITS)
        cdef float value = frac * consts.NORMAL_RESOLUTION

        return -value if sign_bit else value

    cpdef float read_bit_coord(self):
        """Read a float and treat as a world coordinate.

        :returns: float
        """
        cdef bint integer = self.read_bit()
        cdef bint fraction = self.read_bit()
        cdef bint sign_bit = 0
        cdef unsigned int int_val = 0
        cdef unsigned int frac_val = 0
        cdef float ret = 0.0

        if not integer and not fraction:
            return 0.0

        sign_bit = self.read_bit()

        if integer:
            int_val = self.read_uint_bits(consts.COORD_INTEGER_BITS) + 1

        if fraction:
            frac_val = self.read_uint_bits(consts.COORD_FRACTIONAL_BITS)

        value = int_val + (frac_val * consts.COORD_RESOLUTION)

        return -value if sign_bit else value

    cpdef float read_bit_cell_coord(self, unsigned int bits,
                                    unsigned int coord_type):
        """Read a cell coordinate.

        A cell coordinate is a float which has been
        compressed. The number of bits indicates maximum
        value.

        :param bits: number of bits to read
        :type bits: unsigned int
        :param coord_type: level of precision
        :type coord_type: unsigned int
        :returns: float
        """

        cdef bint low_precision = (coord_type == consts.CW_LowPrecision)
        cdef float value = 0.0
        cdef float resolution = 0.0
        cdef unsigned int frac_bits = 0
        cdef unsigned int int_val, frac_val

        if coord_type == consts.CW_Integral:
            value = self.read_uint_bits(bits)
        else:
            if coord_type == consts.COORD_FRACTIONAL_BITS_MP_LOWPRECISION:
                frac_bits = low_precision
            else:
                frac_bits = consts.COORD_FRACTIONAL_BITS

            if low_precision:
                resolution = consts.COORD_RESOLUTION_LOWPRECISION
            else:
                resolution = consts.COORD_RESOLUTION

            int_val = self.read_uint_bits(bits)
            frac_val = self.read_uint_bits(frac_bits)

            value = int_val + (frac_val * resolution)

        return value

    cpdef bytes read_user_data(self, unsigned int bits):
        """Read user data.

        :param bits: Number of bits to read
        :type bits: unsigned int
        :returns: bytes
        """
        cdef unsigned int entries = int(ceil(bits / 8.0))
        cdef array.array[unsigned char] ret = array.array('B', [0] * entries)
        cdef unsigned int arr_idx = 0

        if bits % 8 == 0:
            while bits != 0:
                ret[arr_idx] = self.read_uint_bits(8)
                bits -= 8
                arr_idx += 1
            return bytes(ret)

        arr_idx = 0
        while bits >= 8:
            ret[arr_idx] = self.read_uint_bits(8)
            arr_idx += 1
            bits -= 8

        if bits > 0:
            ret[arr_idx] = self.read_uint_bits(bits)

        return bytes(ret)
