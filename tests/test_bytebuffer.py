from demoparser.bytebuffer import Bytebuffer
from demoparser import structures


def test_read():
    b = Bytebuffer(b'\x01\x02\x03')
    assert b.read(3) == b'\x01\x02\x03'


def test_read_command_header():
    b = Bytebuffer(b'\x01\x02\x03\x04\x05\x06')
    header = b.read_command_header()

    assert type(header) == structures.CommandHeader
    assert header.command == 1
    assert header.tick == 84148994
    assert header.player == 6
