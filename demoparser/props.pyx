from cython.operator cimport dereference
from demoparser.bitbuffer cimport Bitbuffer
from demoparser import consts

from libc.math cimport ceil, log2, sqrt, NAN, isnan
cimport cython


cdef class Decoder:
    """Decode a property.

    Properties of server classes are encoded differently depending
    on the type of the property.

    :param buf: Raw buffer data used for decoding
    :type buf: Bitbuffer
    :param prop: Property to decode
    :type prop: object
    """

    def __cinit__(self, Bitbuffer buf, object prop):
        self.buf = buf
        self.fprop = prop
        self.prop = prop['prop']
        self.flags = self.prop.flags

    cpdef object decode(self):
        assert self.prop.type != PropTypes.DPT_DataTable
        cdef unsigned char prop_type = self.prop.type

        if prop_type == PropTypes.DPT_Int:
            ret = self.decode_int()
        elif prop_type == PropTypes.DPT_Float:
            ret = self.decode_float()
        elif prop_type == PropTypes.DPT_Vector:
            ret = self.decode_vector()
        elif prop_type == PropTypes.DPT_VectorXY:
            ret = self.decode_vector_xy()
        elif prop_type == PropTypes.DPT_String:
            ret = self.decode_string()
        elif prop_type == PropTypes.DPT_Int64:
            ret = self.decode_int64()
        elif prop_type == PropTypes.DPT_Array:
            ret = self.decode_array()
        else:
            raise Exception("Unsupported prop type")

        return ret

    cpdef long decode_int(self):
        """Decode an integer.

        Reads the number of bits specified in the
        num_bits field of the property. If the property
        has the SPROP_UNSIGNED flag set the number will be
        read as an unsigned int.
        """
        cdef long ret
        cdef int num_bits = self.prop.num_bits

        if self.flags & PropFlags.SPROP_UNSIGNED != 0:
            if num_bits == 1:
                ret = self.buf.read_bit()
            else:
                ret = self.buf.read_uint_bits(num_bits)
        else:
            ret = self.buf.read_sint_bits(num_bits)
        return ret

    @cython.cdivision(True)
    cpdef float decode_float(self):
        """Decode a floating point value.

        First the value is decoded as a special float. If that
        returns NaN then a normal floating point value is calculated.
        """
        cdef float special = self.decode_special_float()
        if not isnan(special):
            return special

        cdef int interp
        cdef float val
        cdef int num_bits = self.prop.num_bits
        cdef float high_value = self.prop.high_value
        cdef float low_value = self.prop.low_value

        interp = self.buf.read_uint_bits(num_bits)
        val = interp / ((1 << num_bits) - 1)
        val = low_value + (high_value - low_value) * val

        return val

    cpdef dict decode_vector(self):
        """Decode a vector.

        :returns: vector
        """
        cdef bint sign
        cdef float sum_sqr, x, y, z

        x = self.decode_float()
        y = self.decode_float()

        if (self.flags & PropFlags.SPROP_NORMAL) == 0:
            z = self.decode_float()
        else:
            sign = self.buf.read_bit()
            sum_sqr = (x * x) + (y * y)
            if sum_sqr < 1.0:
                z = sqrt(1.0 - sum_sqr)
            else:
                z = 0.0

            if sign:
                z = -z

        return {
            'x': x,
            'y': y,
            'z': z
        }

    cpdef dict decode_vector_xy(self):
        """Decode a two-element vector.

        This only reads the X and Y coordinates for
        the vector and sets the Z coordinate to 0.0

        :returns: vector
        """
        cdef float x, y
        x = self.decode_float()
        y = self.decode_float()
        return {
            'x': x,
            'y': y,
            'z': 0.0
        }

    cpdef str decode_string(self):
        r"""Decode a string.

        A fixed number of bits are read which may be
        more than the string's length (i.e. some bits
        are read after a \0 is encountered).

        :returns: str
        """
        cdef unsigned int length = self.buf.read_uint_bits(9)
        if not length:
            return ""
        string = self.buf.read_string(length)
        return string

    def decode_int64(self):
        """Decode a 64-bit integer.

        CS:GO demos don't appear to contain 64-bit ints.
        """
        assert False, 'int64'

    cpdef list decode_array(self):
        """Decode array.

        Arrays contain one or more elements (including arrays) which
        are recursively decoded.
        """
        cdef unsigned int bits, idx, num_elements

        max_elements = self.prop.num_elements
        bits = (<unsigned int>ceil(log2(max_elements))) + 1
        num_elements = self.buf.read_uint_bits(bits)

        elements = []
        for idx in range(num_elements):
            prop = {'prop': self.fprop['array_element_prop']}
            val = Decoder(self.buf, prop).decode()
            elements.append(val)

        return elements

    cpdef float decode_special_float(self):
        """Decode a float

        A special float is a float which is interpreted in
        some special way. The treatement is determined by
        the property's flags.

        +-------------------------+--------------------------------------+
        | Flag                    | Explanation                          |
        +=========================+======================================+
        | COORD                   | Treat the float or vector as a world |
        |                         | coordinate.                          |
        +-------------------------+--------------------------------------+
        | COORD_MP                | Like COORD but special handling for  |
        |                         | multi-player games.                  |
        +-------------------------+--------------------------------------+
        | COORD_MP_LOWPRECISION   | Like COORD_MP but the fractional     |
        |                         | component uses 3 bits instead of 5.  |
        +-------------------------+--------------------------------------+
        | COORD_MP_INTEGRAL       | Like COORD_MP but coordinates are    |
        |                         | rounded to integral boundaries.      |
        +-------------------------+--------------------------------------+
        | NOSCALE                 | Don't scale floating-point value to  |
        |                         | a range.                             |
        +-------------------------+--------------------------------------+
        | NORMAL                  | Treat vector as a normal.            |
        +-------------------------+--------------------------------------+
        | CELL_COORD              | Like COORD but has special encoding  |
        |                         | for cell coordinates which can't be  |
        |                         | negative.                            |
        +-------------------------+--------------------------------------+
        | CELL_COORD_LOWPRECISION | Like CELL_COORD but fractional part  |
        |                         | uses 3 bits instead of 5.            |
        +-------------------------+--------------------------------------+
        | CELL_COORD_INTEGRAL     | Like CELL_COORD but coordinates are  |
        |                         | rounded to integral boundaries.      |
        +-------------------------+--------------------------------------+
        """
        cdef float val = NAN
        cdef unsigned int f
        cdef unsigned int flags = self.flags

        if flags & PropFlags.SPROP_COORD:
            val = self.buf.read_bit_coord()
        elif flags & PropFlags.SPROP_COORD_MP:
            val = self.buf.read_bit_coord_mp(consts.CW_None)
        elif flags & PropFlags.SPROP_COORD_MP_LOWPRECISION:
            val = self.buf.read_bit_coord_mp(consts.CW_LowPrecision)
        elif flags & PropFlags.SPROP_COORD_MP_INTEGRAL:
            val = self.buf.read_bit_coord_mp(consts.CW_Integral)
        elif flags & PropFlags.SPROP_NOSCALE:
            f = self.buf.read_uint_bits(32)
            val = dereference(<float *>&f)
        elif flags & PropFlags.SPROP_NORMAL:
            val = self.buf.read_bit_normal()
        elif flags & PropFlags.SPROP_CELL_COORD:
            val = self.buf.read_bit_cell_coord(
                self.prop.num_bits, consts.CW_None
            )
        elif flags & PropFlags.SPROP_CELL_COORD_LOWPRECISION:
            val = self.buf.read_bit_cell_coord(
                self.prop.num_bits, consts.CW_LowPrecision
            )
        elif flags & PropFlags.SPROP_CELL_COORD_INTEGRAL:
            val = self.buf.read_bit_cell_coord(
                self.prop.num_bits, consts.CW_Integral
            )

        return val
