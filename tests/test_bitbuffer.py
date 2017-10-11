from demoparser.bitbuffer import Bitbuffer


def test_read_bit():
    b = Bitbuffer(b'\xff\xff\xff\xff\x00')

    # Bitbuffer reads 32-bits at a time so 32 bits must be
    # read to check that it moves to the next word correctly.
    bits = [b.read_bit() for i in range(32)]
    assert bits == [1] * 32

    # Next word is 0 so next bit should be 0
    assert b.read_bit() == 0


def test_read_uint_bits():
    # Buffer is shown below and the word boundary is marked by ||.
    # 00100001000111111111000000000011 || 00110010
    b = Bitbuffer(b'\x00\xff\x11\x22\x33')

    # Read 0010000100011111111100000000
    num = b.read_uint_bits(28)
    assert num == 34733824

    # Test reading integers across word bundary
    # This will read the final 0011 from the first word
    # followed by 00110010 for a total of 12 bits. This value
    # should equal 001100110010.
    num = b.read_uint_bits(12)
    assert num == 818


def test_read_sint_bits():
    # 10000010
    b = Bitbuffer(b'\x82')
    num = b.read_sint_bits(8)
    assert num == -126

    # Unsigned this time
    # 00000010
    b = Bitbuffer(b'\x02')
    num = b.read_sint_bits(8)
    assert num == 2


def test_read_string():

    # Read until \0
    b = Bitbuffer(b'test\x00more\xff')
    assert b.read_string() == 'test'

    # Next value will be 'm'
    assert chr(b.read_uint_bits(8)) == 'm'

    # Read a fixed length
    # \x00more has been read but not returned
    b = Bitbuffer(b'test\x00more\xff')
    assert b.read_string(9) == 'test'

    # All that sould be left is \xff which is 255
    assert b.read_uint_bits(8) == 255
