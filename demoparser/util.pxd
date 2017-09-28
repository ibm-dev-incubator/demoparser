from demoparser.bitbuffer cimport Bitbuffer

cdef int read_field_index(Bitbuffer buf, int last_index, bint new_way)
cdef list parse_entity_update(Bitbuffer buf, object server_class)
