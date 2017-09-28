from suitcase.structure import Structure
from suitcase.fields import Magic
from suitcase.fields import SubstructureField
from suitcase.fields import UBInt8Sequence
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
    view_origin = Vector()
    view_angles = QAngle()
    local_view_angles = QAngle()


class SplitCommandInfo(Structure):
    flags = ULInt32()
    original = SubstructureField(OriginViewAngles)
    resampled = SubstructureField(OriginViewAngles)


class CommandInfo(Structure):
    command_1 = SplitCommandInfo
    command_2 = SplitCommandInfo


class UserInfo(Structure):
    tbd = UBInt64()
    xuid = UBInt64()
    name = FixedLengthString(consts.MAX_PLAYER_NAME_LENGTH)
    user_id = UBInt32()
    guid = FixedLengthString(consts.SIGNED_GUID_LEN)
    skip1 = UBInt8Sequence(3)
    friends_id = UBInt32()
    friends_name = FixedLengthString(consts.MAX_PLAYER_NAME_LENGTH)
    fake_player = UBInt8()
    skip2 = UBInt8Sequence(3)
    is_hltv = UBInt8()
    skip3 = UBInt8Sequence(3)
    custom_files = UBInt32Sequence(consts.MAX_CUSTOM_FILES)
