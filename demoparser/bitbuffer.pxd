cdef class Bitbuffer:
    cdef public unsigned int num_bytes
    cdef public unsigned int num_bits
    cdef unsigned int * data
    cdef unsigned int index
    cdef unsigned int length
    cdef unsigned int bits_avail
    cdef unsigned int in_buf_word
    cdef bytes orig_data

    cpdef unsigned int next_dword(self)
    cpdef unsigned char read_bit(self)
    cpdef unsigned int read_uint_bits(self, unsigned int bits)
    cpdef int read_sint_bits(self, unsigned int bits)
    cpdef unsigned int read_var_int(self)
    cpdef str read_string(self, int length=*)
    cpdef float read_bit_normal(self)
    cpdef float read_bit_coord(self)
    cpdef float read_bit_cell_coord(self, unsigned int bits,
            unsigned int coord_type)
    cpdef bytes read_user_data(self, unsigned int bits)
