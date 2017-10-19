import pytest

from demoparser.demofile import CommandError
from demoparser.demofile import DemoFile
from demoparser.structures import CommandHeader


def test_parse_invalid_command():
    # Demo files have a 1072 byte header that isn't needed here
    data = b'HL2DEMO\x00' + bytes([0] * 1064)
    header = CommandHeader()
    header.player = 1
    header.tick = 1
    header.command = 99

    df = DemoFile(data + header.pack())
    with pytest.raises(CommandError) as exc:
        df.parse()

    assert 'Unrecognized command' in str(exc.value)
