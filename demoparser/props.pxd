from demoparser.bitbuffer cimport Bitbuffer

cdef class Decoder:
    cdef Bitbuffer buf
    cdef dict fprop
    cdef object prop
    cdef long flags

    # Methods
    cdef object decode(self)
    cdef long _decode_int(self)
    cdef float _decode_float(self)
    cdef dict _decode_vector(self)
    cdef dict _decode_vector_xy(self)
    cdef str _decode_string(self)
    cdef list _decode_array(self)
    cdef float _decode_special_float(self)

cdef enum PropTypes:
    DPT_Int = 0
    DPT_Float = 1
    DPT_Vector = 2
    DPT_VectorXY = 3
    DPT_String = 4
    DPT_Array = 5
    DPT_DataTable = 6
    DPT_Int64 = 7
    DT_MAX_STRING_BITS = 9

cdef enum PropFlags:
    SPROP_UNSIGNED = (1 << 0)
    SPROP_COORD = (1 << 1)
    SPROP_NOSCALE = (1 << 2)
    SPROP_ROUNDDOWN = (1 << 3)
    SPROP_ROUNDUP = (1 << 4)
    SPROP_NORMAL = (1 << 5)
    SPROP_EXCLUDE = (1 << 6)
    SPROP_XYZE = (1 << 7)
    SPROP_INSIDEARRAY = (1 << 8)
    SPROP_PROXY_ALWAYS_YES = (1 << 9)
    SPROP_IS_A_VECTOR_ELEM = (1 << 10)
    SPROP_COLLAPSIBLE = (1 << 11)
    SPROP_COORD_MP = (1 << 12)
    SPROP_COORD_MP_LOWPRECISION = (1 << 13)
    SPROP_COORD_MP_INTEGRAL = (1 << 14)
    SPROP_CELL_COORD = (1 << 15)
    SPROP_CELL_COORD_LOWPRECISION = (1 << 16)
    SPROP_CELL_COORD_INTEGRAL = (1 << 17)
    SPROP_CHANGES_OFTEN = (1 << 18)
    SPROP_VARINT = (1 << 19)
