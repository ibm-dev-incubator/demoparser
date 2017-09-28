cdef class Bitbuffer:
    cdef public unsigned int num_bytes
    cdef public unsigned int num_bits
    cdef unsigned int * data
    cdef unsigned int index
    cdef unsigned int length
    cdef unsigned int bits_avail
    cdef unsigned int in_buf_word
    cdef bytes orig_data

    cdef unsigned int next_dword(self)
    cdef unsigned char read_bit(self)
    cdef unsigned int read_uint_bits(self, unsigned int bits)
    cdef int read_sint_bits(self, unsigned int bits)
    cdef unsigned int read_var_int(self)
    cdef str read_string(self, int length=*)
    cdef float read_bit_normal(self)
    cdef float read_bit_coord(self)
    cdef float read_bit_cell_coord(self, unsigned int bits,
            unsigned int coord_type)
    cdef bytes read_user_data(self, unsigned int bits)
