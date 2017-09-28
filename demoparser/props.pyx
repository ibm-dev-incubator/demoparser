# cython: profile=True
from cython.operator cimport dereference
from demoparser.bitbuffer cimport Bitbuffer
from demoparser import consts

from libc.math cimport ceil, log2, sqrt, NAN, isnan
cimport cython


cdef class Decoder:

    def __cinit__(self, Bitbuffer buf, object prop):
        self.buf = buf
        self.fprop = prop
        self.prop = prop['prop']
        self.flags = self.prop.flags

    cdef object decode(self):
        assert self.prop.type != PropTypes.DPT_DataTable
        cdef unsigned char prop_type = self.prop.type

        if prop_type == PropTypes.DPT_Int:
            ret = self._decode_int()
        elif prop_type == PropTypes.DPT_Float:
            ret = self._decode_float()
        elif prop_type == PropTypes.DPT_Vector:
            ret = self._decode_vector()
        elif prop_type == PropTypes.DPT_VectorXY:
            ret = self._decode_vector_xy()
        elif prop_type == PropTypes.DPT_String:
            ret = self._decode_string()
        elif prop_type == PropTypes.DPT_Int64:
            ret = self._decode_int64()
        elif prop_type == PropTypes.DPT_Array:
            ret = self._decode_array()
        else:
            raise Exception("Unsupported prop type")

        return ret

    cdef long _decode_int(self):
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
    cdef float _decode_float(self):
        cdef float special = self._decode_special_float()
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

    cdef dict _decode_vector(self):
        cdef bint sign
        cdef float sum_sqr, x, y, z

        x = self._decode_float()
        y = self._decode_float()

        if (self.flags & PropFlags.SPROP_NORMAL) == 0:
            z = self._decode_float()
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

    cdef dict _decode_vector_xy(self):
        cdef float x, y
        x = self._decode_float()
        y = self._decode_float()
        return {
            'x': x,
            'y': y,
            'z': 0.0
        }

    cdef str _decode_string(self):
        cdef unsigned int length = self.buf.read_uint_bits(9)
        if not length:
            return ""
        string = self.buf.read_string(length)
        return string

    def _decode_int64(self):
        assert False, 'int64'

    cdef list _decode_array(self):
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

    cdef float _decode_special_float(self):
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
