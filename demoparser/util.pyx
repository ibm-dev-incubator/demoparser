# cython: profile=True
from demoparser.bitbuffer cimport Bitbuffer
from demoparser.props cimport Decoder
from demoparser.props cimport PropFlags
from demoparser.props cimport PropTypes

cpdef int read_field_index(Bitbuffer buf, int last_index, bint new_way):
    """Read index.

    This method determines the next index into the property
    list for server class.

    :returns: Next index or -1 if no more indices
    """
    cdef int ret = 0
    cdef unsigned int val = 0

    if new_way and buf.read_bit():
        return last_index + 1

    if new_way and buf.read_bit():
        ret = buf.read_uint_bits(3)
    else:
        ret = buf.read_uint_bits(7)
        val = ret & (32 | 64)

        if val == 32:
            ret = (ret & ~96) | (buf.read_uint_bits(2) << 5)
            assert ret >= 32
        elif val == 64:
            ret = (ret & ~96) | (buf.read_uint_bits(4) << 5)
            assert ret >= 128
        elif val == 96:
            ret = (ret & ~96) | (buf.read_uint_bits(7) << 5)
            assert ret >= 512

    if ret == 0xfff:
        return -1

    return last_index + 1 + ret


cpdef list parse_entity_update(Bitbuffer buf, object server_class):
    """Parse entity updates.

    First a list of all property indices is generated. For each
    property referenced by those indices the property's value is
    decoded. The list of properties and their decoded values are
    collected and returned.

    :returns: List of updated properties
    """
    cdef bint new_way
    cdef int val = -1
    cdef Decoder decoder

    updated_props = []
    field_indices = []

    new_way = buf.read_bit()

    while True:
        val = read_field_index(buf, val, new_way)

        if val == -1:
            break

        field_indices.append(val)

    for index in field_indices:
        flattened_prop = server_class['props'][index]

        decoder = Decoder.__new__(Decoder, buf, flattened_prop)

        updated_props.append({
            'prop': flattened_prop,
            'value': decoder.decode()
        })

    return updated_props
