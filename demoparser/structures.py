from suitcase.structure import Structure
from suitcase.fields import FieldArray
from suitcase.fields import Magic
from suitcase.fields import SubstructureField
from suitcase.fields import ULInt32
from suitcase.fields import UBInt32
from suitcase.fields import UBInt64
from suitcase.fields import UBInt8
from suitcase.fields import ULInt8

from demoparser import consts
from demoparser.fields import FixedLengthString
from demoparser.fields import SLFloat32
from demoparser.fields import UBInt32Sequence


class DemoHeader(Structure):
    r"""1072 Byte header for .DEM file.

    This header has the following format:

    +-----------+---------------------------------------+
    | Byte      | Description                           |
    +===========+=======================================+
    | 0-7       | Fixed string 'HL2DEMO\0'.             |
    +-----------+---------------------------------------+
    | 8-11      | Demo file protocol version.           |
    +-----------+---------------------------------------+
    | 12-15     | Network protocol version.             |
    +-----------+---------------------------------------+
    | 16-275    | Server name.                          |
    +-----------+---------------------------------------+
    | 276-535   | Name of client who recorded the demo. |
    +-----------+---------------------------------------+
    | 536-795   | Map name.                             |
    +-----------+---------------------------------------+
    | 796-1055  | Game directory.                       |
    +-----------+---------------------------------------+
    | 1056-1059 | Playback time in seconds.             |
    +-----------+---------------------------------------+
    | 1060-1063 | Number of ticks in demo.              |
    +-----------+---------------------------------------+
    | 1064-1067 | Number of frames in demo.             |
    +-----------+---------------------------------------+
    | 1068-1071 | Length of signon data.                |
    +-----------+---------------------------------------+
    """
    header = Magic(b'HL2DEMO\x00')
    demo_protocol = ULInt32()
    network_protocol = ULInt32()
    server_name = FixedLengthString(consts.MAX_PATH)
    client_name = FixedLengthString(consts.MAX_PATH)
    map_name = FixedLengthString(consts.MAX_PATH)
    game_directory = FixedLengthString(consts.MAX_PATH)
    playback_time = SLFloat32()
    ticks = ULInt32()
    frames = ULInt32()
    signon_length = ULInt32()


class CommandHeader(Structure):
    """Header for each command packet.

    .. _header-format:

    The header has the following format:

    +------+--------------+
    | Byte | Description  |
    +======+==============+
    | 0    | Command ID   |
    +------+--------------+
    | 1-4  | Current tick |
    +------+--------------+
    | 5    | Player ID    |
    +------+--------------+
    """
    command = ULInt8()
    tick = ULInt32()
    player = ULInt8()


class QAngle(Structure):
    pitch = SLFloat32()
    yaw = SLFloat32()
    roll = SLFloat32()


class Vector(Structure):
    x = SLFloat32()
    y = SLFloat32()
    z = SLFloat32()


class OriginViewAngles(Structure):
    view_origin = SubstructureField(Vector)
    view_angles = SubstructureField(QAngle)
    local_view_angles = SubstructureField(QAngle)


class SplitCommandInfo(Structure):
    flags = ULInt32()
    original = SubstructureField(OriginViewAngles)
    resampled = SubstructureField(OriginViewAngles)


class CommandInfo(Structure):
    commands = FieldArray(SplitCommandInfo)


class UserInfo(Structure):
    """Player data.

    This structure has the following format:

    +---------+---------------------------------------+
    | Byte    | Description                           |
    +=========+=======================================+
    | 0-7     | Version. Same for all players.        |
    +---------+---------------------------------------+
    | 8-15    | xuid. Some sort of unique ID.         |
    +---------+---------------------------------------+
    | 15-142  | Player name.                          |
    +---------+---------------------------------------+
    | 143-146 | Local server user ID.                 |
    +---------+---------------------------------------+
    | 147-179 | GUID                                  |
    +---------+---------------------------------------+
    | 180-183 | Friend's ID.                          |
    +---------+---------------------------------------+
    | 184-312 | Friend's Name.                        |
    +---------+---------------------------------------+
    | 313     | Is player a bot?                      |
    +---------+---------------------------------------+
    | 314     | Is player an HLTV proxy?              |
    +---------+---------------------------------------+
    | 314-329 | Custom files CRC.                     |
    +---------+---------------------------------------+
    | 330     | Numbre of files downloaded by server. |
    +---------+---------------------------------------+
    | 331-335 | Entity index.                         |
    +---------+---------------------------------------+
    | 336-340 | No idea.                              |
    +---------+---------------------------------------+
    """
    version = UBInt64()
    xuid = UBInt64()
    name = FixedLengthString(consts.MAX_PLAYER_NAME_LENGTH)
    user_id = UBInt32()
    guid = FixedLengthString(consts.SIGNED_GUID_LEN)
    friends_id = UBInt32()
    friends_name = FixedLengthString(consts.MAX_PLAYER_NAME_LENGTH)
    fake_player = UBInt8()
    is_hltv = UBInt8()
    custom_files = UBInt32Sequence(consts.MAX_CUSTOM_FILES)
    files_downloaded = UBInt8()
    entity_id = UBInt32()
    tbd = UBInt32()
