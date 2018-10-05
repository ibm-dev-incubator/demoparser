# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: network_connection.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='network_connection.proto',
  package='',
  syntax='proto2',
  serialized_options=_b('\200\001\000'),
  serialized_pb=_b('\n\x18network_connection.proto\x1a google/protobuf/descriptor.proto*\x8c%\n\x1b\x45NetworkDisconnectionReason\x12\x1e\n\x1aNETWORK_DISCONNECT_INVALID\x10\x00\x12\x1f\n\x1bNETWORK_DISCONNECT_SHUTDOWN\x10\x01\x12\x46\n%NETWORK_DISCONNECT_DISCONNECT_BY_USER\x10\x02\x1a\x1b\xa2\xd4\x18\x17#GameUI_Disconnect_User\x12J\n\'NETWORK_DISCONNECT_DISCONNECT_BY_SERVER\x10\x03\x1a\x1d\xa2\xd4\x18\x19#GameUI_Disconnect_Server\x12\x42\n\x17NETWORK_DISCONNECT_LOST\x10\x04\x1a%\xa2\xd4\x18!#GameUI_Disconnect_ConnectionLost\x12J\n\x1bNETWORK_DISCONNECT_OVERFLOW\x10\x05\x1a)\xa2\xd4\x18%#GameUI_Disconnect_ConnectionOverflow\x12I\n\x1fNETWORK_DISCONNECT_STEAM_BANNED\x10\x06\x1a$\xa2\xd4\x18 #GameUI_Disconnect_SteamIDBanned\x12G\n\x1eNETWORK_DISCONNECT_STEAM_INUSE\x10\x07\x1a#\xa2\xd4\x18\x1f#GameUI_Disconnect_SteamIDInUse\x12G\n\x1fNETWORK_DISCONNECT_STEAM_TICKET\x10\x08\x1a\"\xa2\xd4\x18\x1e#GameUI_Disconnect_SteamTicket\x12\x45\n\x1eNETWORK_DISCONNECT_STEAM_LOGON\x10\t\x1a!\xa2\xd4\x18\x1d#GameUI_Disconnect_SteamLogon\x12M\n&NETWORK_DISCONNECT_STEAM_AUTHCANCELLED\x10\n\x1a!\xa2\xd4\x18\x1d#GameUI_Disconnect_SteamLogon\x12O\n(NETWORK_DISCONNECT_STEAM_AUTHALREADYUSED\x10\x0b\x1a!\xa2\xd4\x18\x1d#GameUI_Disconnect_SteamLogon\x12K\n$NETWORK_DISCONNECT_STEAM_AUTHINVALID\x10\x0c\x1a!\xa2\xd4\x18\x1d#GameUI_Disconnect_SteamLogon\x12I\n$NETWORK_DISCONNECT_STEAM_VACBANSTATE\x10\r\x1a\x1f\xa2\xd4\x18\x1b#GameUI_Disconnect_SteamVAC\x12S\n,NETWORK_DISCONNECT_STEAM_LOGGED_IN_ELSEWHERE\x10\x0e\x1a!\xa2\xd4\x18\x1d#GameUI_Disconnect_SteamInUse\x12T\n+NETWORK_DISCONNECT_STEAM_VAC_CHECK_TIMEDOUT\x10\x0f\x1a#\xa2\xd4\x18\x1f#GameUI_Disconnect_SteamTimeOut\x12I\n NETWORK_DISCONNECT_STEAM_DROPPED\x10\x10\x1a#\xa2\xd4\x18\x1f#GameUI_Disconnect_SteamDropped\x12M\n\"NETWORK_DISCONNECT_STEAM_OWNERSHIP\x10\x11\x1a%\xa2\xd4\x18!#GameUI_Disconnect_SteamOwnership\x12U\n&NETWORK_DISCONNECT_SERVERINFO_OVERFLOW\x10\x12\x1a)\xa2\xd4\x18%#GameUI_Disconnect_ServerInfoOverflow\x12K\n#NETWORK_DISCONNECT_TICKMSG_OVERFLOW\x10\x13\x1a\"\xa2\xd4\x18\x1e#GameUI_Disconnect_TickMessage\x12Y\n*NETWORK_DISCONNECT_STRINGTABLEMSG_OVERFLOW\x10\x14\x1a)\xa2\xd4\x18%#GameUI_Disconnect_StringTableMessage\x12S\n\'NETWORK_DISCONNECT_DELTAENTMSG_OVERFLOW\x10\x15\x1a&\xa2\xd4\x18\"#GameUI_Disconnect_DeltaEntMessage\x12Q\n&NETWORK_DISCONNECT_TEMPENTMSG_OVERFLOW\x10\x16\x1a%\xa2\xd4\x18!#GameUI_Disconnect_TempEntMessage\x12O\n%NETWORK_DISCONNECT_SOUNDSMSG_OVERFLOW\x10\x17\x1a$\xa2\xd4\x18 #GameUI_Disconnect_SoundsMessage\x12P\n#NETWORK_DISCONNECT_SNAPSHOTOVERFLOW\x10\x18\x1a\'\xa2\xd4\x18##GameUI_Disconnect_SnapshotOverflow\x12J\n NETWORK_DISCONNECT_SNAPSHOTERROR\x10\x19\x1a$\xa2\xd4\x18 #GameUI_Disconnect_SnapshotError\x12P\n#NETWORK_DISCONNECT_RELIABLEOVERFLOW\x10\x1a\x1a\'\xa2\xd4\x18##GameUI_Disconnect_ReliableOverflow\x12N\n\x1fNETWORK_DISCONNECT_BADDELTATICK\x10\x1b\x1a)\xa2\xd4\x18%#GameUI_Disconnect_BadClientDeltaTick\x12H\n\x1fNETWORK_DISCONNECT_NOMORESPLITS\x10\x1c\x1a#\xa2\xd4\x18\x1f#GameUI_Disconnect_NoMoreSplits\x12@\n\x1bNETWORK_DISCONNECT_TIMEDOUT\x10\x1d\x1a\x1f\xa2\xd4\x18\x1b#GameUI_Disconnect_TimedOut\x12H\n\x1fNETWORK_DISCONNECT_DISCONNECTED\x10\x1e\x1a#\xa2\xd4\x18\x1f#GameUI_Disconnect_Disconnected\x12H\n\x1fNETWORK_DISCONNECT_LEAVINGSPLIT\x10\x1f\x1a#\xa2\xd4\x18\x1f#GameUI_Disconnect_LeavingSplit\x12X\n\'NETWORK_DISCONNECT_DIFFERENTCLASSTABLES\x10 \x1a+\xa2\xd4\x18\'#GameUI_Disconnect_DifferentClassTables\x12P\n#NETWORK_DISCONNECT_BADRELAYPASSWORD\x10!\x1a\'\xa2\xd4\x18##GameUI_Disconnect_BadRelayPassword\x12X\n\'NETWORK_DISCONNECT_BADSPECTATORPASSWORD\x10\"\x1a+\xa2\xd4\x18\'#GameUI_Disconnect_BadSpectatorPassword\x12L\n!NETWORK_DISCONNECT_HLTVRESTRICTED\x10#\x1a%\xa2\xd4\x18!#GameUI_Disconnect_HLTVRestricted\x12H\n\x1fNETWORK_DISCONNECT_NOSPECTATORS\x10$\x1a#\xa2\xd4\x18\x1f#GameUI_Disconnect_NoSpectators\x12N\n\"NETWORK_DISCONNECT_HLTVUNAVAILABLE\x10%\x1a&\xa2\xd4\x18\"#GameUI_Disconnect_HLTVUnavailable\x12@\n\x1bNETWORK_DISCONNECT_HLTVSTOP\x10&\x1a\x1f\xa2\xd4\x18\x1b#GameUI_Disconnect_HLTVStop\x12<\n\x19NETWORK_DISCONNECT_KICKED\x10\'\x1a\x1d\xa2\xd4\x18\x19#GameUI_Disconnect_Kicked\x12@\n\x1bNETWORK_DISCONNECT_BANADDED\x10(\x1a\x1f\xa2\xd4\x18\x1b#GameUI_Disconnect_BanAdded\x12H\n\x1fNETWORK_DISCONNECT_KICKBANADDED\x10)\x1a#\xa2\xd4\x18\x1f#GameUI_Disconnect_KickBanAdded\x12\x44\n\x1dNETWORK_DISCONNECT_HLTVDIRECT\x10*\x1a!\xa2\xd4\x18\x1d#GameUI_Disconnect_HLTVDirect\x12\\\n)NETWORK_DISCONNECT_PURESERVER_CLIENTEXTRA\x10+\x1a-\xa2\xd4\x18)#GameUI_Disconnect_PureServer_ClientExtra\x12V\n&NETWORK_DISCONNECT_PURESERVER_MISMATCH\x10,\x1a*\xa2\xd4\x18&#GameUI_Disconnect_PureServer_Mismatch\x12>\n\x1aNETWORK_DISCONNECT_USERCMD\x10-\x1a\x1e\xa2\xd4\x18\x1a#GameUI_Disconnect_UserCmd\x12N\n#NETWORK_DISCONNECT_REJECTED_BY_GAME\x10.\x1a%\xa2\xd4\x18!#GameUI_Disconnect_RejectedByGame\x12T\n&NETWORK_DISCONNECT_MESSAGE_PARSE_ERROR\x10/\x1a(\xa2\xd4\x18$#GameUI_Disconnect_MessageParseError\x12X\n(NETWORK_DISCONNECT_INVALID_MESSAGE_ERROR\x10\x30\x1a*\xa2\xd4\x18&#GameUI_Disconnect_InvalidMessageError\x12T\n&NETWORK_DISCONNECT_BAD_SERVER_PASSWORD\x10\x31\x1a(\xa2\xd4\x18$#GameUI_Disconnect_BadServerPassword\x12\x62\n-NETWORK_DISCONNECT_DIRECT_CONNECT_RESERVATION\x10\x32\x1a/\xa2\xd4\x18+#GameUI_Disconnect_DirectConnectReservation\x12S\n%NETWORK_DISCONNECT_CONNECTION_FAILURE\x10\x33\x1a(\xa2\xd4\x18$#GameUI_Disconnect_ConnectionFailure\x12Y\n)NETWORK_DISCONNECT_NO_PEER_GROUP_HANDLERS\x10\x34\x1a*\xa2\xd4\x18&#GameUI_Disconnect_NoPeerGroupHandlers\x12H\n\x1fNETWORK_DISCONNECT_RECONNECTION\x10\x35\x1a#\xa2\xd4\x18\x1f#GameUI_Disconnect_Reconnection\x12S\n%NETWORK_DISCONNECT_CONNECTION_CLOSING\x10\x36\x1a(\xa2\xd4\x18$#GameUI_Disconnect_ConnectionClosing\x12]\n+NETWORK_DISCONNECT_NO_GOTV_RELAYS_AVAILABLE\x10\x37\x1a,\xa2\xd4\x18(#GameUI_Disconnect_NoGOTVRelaysAvailable\x12O\n#NETWORK_DISCONNECT_SESSION_MIGRATED\x10\x38\x1a&\xa2\xd4\x18\"#GameUI_Disconnect_SessionMigrated\x12\x62\n,NETWORK_DISCONNECT_VERYLARGETRANSFEROVERFLOW\x10\x39\x1a\x30\xa2\xd4\x18,#GameUI_Disconnect_VeryLargeTransferOverflow\x12N\n\"NETWORK_DISCONNECT_SENDNETOVERFLOW\x10:\x1a&\xa2\xd4\x18\"#GameUI_Disconnect_SendNetOverflow\x12l\n3NETWORK_DISCONNECT_PLAYER_REMOVED_FROM_HOST_SESSION\x10;\x1a\x33\xa2\xd4\x18/#GameUI_Disconnect_PlayerRemovedFromHostSession:E\n\x18network_connection_token\x12!.google.protobuf.EnumValueOptions\x18\xc4\x8a\x03 \x01(\tB\x03\x80\x01\x00')
  ,
  dependencies=[google_dot_protobuf_dot_descriptor__pb2.DESCRIPTOR,])

_ENETWORKDISCONNECTIONREASON = _descriptor.EnumDescriptor(
  name='ENetworkDisconnectionReason',
  full_name='ENetworkDisconnectionReason',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_INVALID', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_SHUTDOWN', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_DISCONNECT_BY_USER', index=2, number=2,
      serialized_options=_b('\242\324\030\027#GameUI_Disconnect_User'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_DISCONNECT_BY_SERVER', index=3, number=3,
      serialized_options=_b('\242\324\030\031#GameUI_Disconnect_Server'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_LOST', index=4, number=4,
      serialized_options=_b('\242\324\030!#GameUI_Disconnect_ConnectionLost'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_OVERFLOW', index=5, number=5,
      serialized_options=_b('\242\324\030%#GameUI_Disconnect_ConnectionOverflow'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_STEAM_BANNED', index=6, number=6,
      serialized_options=_b('\242\324\030 #GameUI_Disconnect_SteamIDBanned'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_STEAM_INUSE', index=7, number=7,
      serialized_options=_b('\242\324\030\037#GameUI_Disconnect_SteamIDInUse'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_STEAM_TICKET', index=8, number=8,
      serialized_options=_b('\242\324\030\036#GameUI_Disconnect_SteamTicket'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_STEAM_LOGON', index=9, number=9,
      serialized_options=_b('\242\324\030\035#GameUI_Disconnect_SteamLogon'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_STEAM_AUTHCANCELLED', index=10, number=10,
      serialized_options=_b('\242\324\030\035#GameUI_Disconnect_SteamLogon'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_STEAM_AUTHALREADYUSED', index=11, number=11,
      serialized_options=_b('\242\324\030\035#GameUI_Disconnect_SteamLogon'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_STEAM_AUTHINVALID', index=12, number=12,
      serialized_options=_b('\242\324\030\035#GameUI_Disconnect_SteamLogon'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_STEAM_VACBANSTATE', index=13, number=13,
      serialized_options=_b('\242\324\030\033#GameUI_Disconnect_SteamVAC'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_STEAM_LOGGED_IN_ELSEWHERE', index=14, number=14,
      serialized_options=_b('\242\324\030\035#GameUI_Disconnect_SteamInUse'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_STEAM_VAC_CHECK_TIMEDOUT', index=15, number=15,
      serialized_options=_b('\242\324\030\037#GameUI_Disconnect_SteamTimeOut'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_STEAM_DROPPED', index=16, number=16,
      serialized_options=_b('\242\324\030\037#GameUI_Disconnect_SteamDropped'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_STEAM_OWNERSHIP', index=17, number=17,
      serialized_options=_b('\242\324\030!#GameUI_Disconnect_SteamOwnership'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_SERVERINFO_OVERFLOW', index=18, number=18,
      serialized_options=_b('\242\324\030%#GameUI_Disconnect_ServerInfoOverflow'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_TICKMSG_OVERFLOW', index=19, number=19,
      serialized_options=_b('\242\324\030\036#GameUI_Disconnect_TickMessage'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_STRINGTABLEMSG_OVERFLOW', index=20, number=20,
      serialized_options=_b('\242\324\030%#GameUI_Disconnect_StringTableMessage'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_DELTAENTMSG_OVERFLOW', index=21, number=21,
      serialized_options=_b('\242\324\030\"#GameUI_Disconnect_DeltaEntMessage'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_TEMPENTMSG_OVERFLOW', index=22, number=22,
      serialized_options=_b('\242\324\030!#GameUI_Disconnect_TempEntMessage'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_SOUNDSMSG_OVERFLOW', index=23, number=23,
      serialized_options=_b('\242\324\030 #GameUI_Disconnect_SoundsMessage'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_SNAPSHOTOVERFLOW', index=24, number=24,
      serialized_options=_b('\242\324\030##GameUI_Disconnect_SnapshotOverflow'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_SNAPSHOTERROR', index=25, number=25,
      serialized_options=_b('\242\324\030 #GameUI_Disconnect_SnapshotError'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_RELIABLEOVERFLOW', index=26, number=26,
      serialized_options=_b('\242\324\030##GameUI_Disconnect_ReliableOverflow'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_BADDELTATICK', index=27, number=27,
      serialized_options=_b('\242\324\030%#GameUI_Disconnect_BadClientDeltaTick'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_NOMORESPLITS', index=28, number=28,
      serialized_options=_b('\242\324\030\037#GameUI_Disconnect_NoMoreSplits'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_TIMEDOUT', index=29, number=29,
      serialized_options=_b('\242\324\030\033#GameUI_Disconnect_TimedOut'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_DISCONNECTED', index=30, number=30,
      serialized_options=_b('\242\324\030\037#GameUI_Disconnect_Disconnected'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_LEAVINGSPLIT', index=31, number=31,
      serialized_options=_b('\242\324\030\037#GameUI_Disconnect_LeavingSplit'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_DIFFERENTCLASSTABLES', index=32, number=32,
      serialized_options=_b('\242\324\030\'#GameUI_Disconnect_DifferentClassTables'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_BADRELAYPASSWORD', index=33, number=33,
      serialized_options=_b('\242\324\030##GameUI_Disconnect_BadRelayPassword'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_BADSPECTATORPASSWORD', index=34, number=34,
      serialized_options=_b('\242\324\030\'#GameUI_Disconnect_BadSpectatorPassword'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_HLTVRESTRICTED', index=35, number=35,
      serialized_options=_b('\242\324\030!#GameUI_Disconnect_HLTVRestricted'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_NOSPECTATORS', index=36, number=36,
      serialized_options=_b('\242\324\030\037#GameUI_Disconnect_NoSpectators'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_HLTVUNAVAILABLE', index=37, number=37,
      serialized_options=_b('\242\324\030\"#GameUI_Disconnect_HLTVUnavailable'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_HLTVSTOP', index=38, number=38,
      serialized_options=_b('\242\324\030\033#GameUI_Disconnect_HLTVStop'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_KICKED', index=39, number=39,
      serialized_options=_b('\242\324\030\031#GameUI_Disconnect_Kicked'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_BANADDED', index=40, number=40,
      serialized_options=_b('\242\324\030\033#GameUI_Disconnect_BanAdded'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_KICKBANADDED', index=41, number=41,
      serialized_options=_b('\242\324\030\037#GameUI_Disconnect_KickBanAdded'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_HLTVDIRECT', index=42, number=42,
      serialized_options=_b('\242\324\030\035#GameUI_Disconnect_HLTVDirect'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_PURESERVER_CLIENTEXTRA', index=43, number=43,
      serialized_options=_b('\242\324\030)#GameUI_Disconnect_PureServer_ClientExtra'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_PURESERVER_MISMATCH', index=44, number=44,
      serialized_options=_b('\242\324\030&#GameUI_Disconnect_PureServer_Mismatch'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_USERCMD', index=45, number=45,
      serialized_options=_b('\242\324\030\032#GameUI_Disconnect_UserCmd'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_REJECTED_BY_GAME', index=46, number=46,
      serialized_options=_b('\242\324\030!#GameUI_Disconnect_RejectedByGame'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_MESSAGE_PARSE_ERROR', index=47, number=47,
      serialized_options=_b('\242\324\030$#GameUI_Disconnect_MessageParseError'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_INVALID_MESSAGE_ERROR', index=48, number=48,
      serialized_options=_b('\242\324\030&#GameUI_Disconnect_InvalidMessageError'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_BAD_SERVER_PASSWORD', index=49, number=49,
      serialized_options=_b('\242\324\030$#GameUI_Disconnect_BadServerPassword'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_DIRECT_CONNECT_RESERVATION', index=50, number=50,
      serialized_options=_b('\242\324\030+#GameUI_Disconnect_DirectConnectReservation'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_CONNECTION_FAILURE', index=51, number=51,
      serialized_options=_b('\242\324\030$#GameUI_Disconnect_ConnectionFailure'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_NO_PEER_GROUP_HANDLERS', index=52, number=52,
      serialized_options=_b('\242\324\030&#GameUI_Disconnect_NoPeerGroupHandlers'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_RECONNECTION', index=53, number=53,
      serialized_options=_b('\242\324\030\037#GameUI_Disconnect_Reconnection'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_CONNECTION_CLOSING', index=54, number=54,
      serialized_options=_b('\242\324\030$#GameUI_Disconnect_ConnectionClosing'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_NO_GOTV_RELAYS_AVAILABLE', index=55, number=55,
      serialized_options=_b('\242\324\030(#GameUI_Disconnect_NoGOTVRelaysAvailable'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_SESSION_MIGRATED', index=56, number=56,
      serialized_options=_b('\242\324\030\"#GameUI_Disconnect_SessionMigrated'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_VERYLARGETRANSFEROVERFLOW', index=57, number=57,
      serialized_options=_b('\242\324\030,#GameUI_Disconnect_VeryLargeTransferOverflow'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_SENDNETOVERFLOW', index=58, number=58,
      serialized_options=_b('\242\324\030\"#GameUI_Disconnect_SendNetOverflow'),
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK_DISCONNECT_PLAYER_REMOVED_FROM_HOST_SESSION', index=59, number=59,
      serialized_options=_b('\242\324\030/#GameUI_Disconnect_PlayerRemovedFromHostSession'),
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=63,
  serialized_end=4811,
)
_sym_db.RegisterEnumDescriptor(_ENETWORKDISCONNECTIONREASON)

ENetworkDisconnectionReason = enum_type_wrapper.EnumTypeWrapper(_ENETWORKDISCONNECTIONREASON)
NETWORK_DISCONNECT_INVALID = 0
NETWORK_DISCONNECT_SHUTDOWN = 1
NETWORK_DISCONNECT_DISCONNECT_BY_USER = 2
NETWORK_DISCONNECT_DISCONNECT_BY_SERVER = 3
NETWORK_DISCONNECT_LOST = 4
NETWORK_DISCONNECT_OVERFLOW = 5
NETWORK_DISCONNECT_STEAM_BANNED = 6
NETWORK_DISCONNECT_STEAM_INUSE = 7
NETWORK_DISCONNECT_STEAM_TICKET = 8
NETWORK_DISCONNECT_STEAM_LOGON = 9
NETWORK_DISCONNECT_STEAM_AUTHCANCELLED = 10
NETWORK_DISCONNECT_STEAM_AUTHALREADYUSED = 11
NETWORK_DISCONNECT_STEAM_AUTHINVALID = 12
NETWORK_DISCONNECT_STEAM_VACBANSTATE = 13
NETWORK_DISCONNECT_STEAM_LOGGED_IN_ELSEWHERE = 14
NETWORK_DISCONNECT_STEAM_VAC_CHECK_TIMEDOUT = 15
NETWORK_DISCONNECT_STEAM_DROPPED = 16
NETWORK_DISCONNECT_STEAM_OWNERSHIP = 17
NETWORK_DISCONNECT_SERVERINFO_OVERFLOW = 18
NETWORK_DISCONNECT_TICKMSG_OVERFLOW = 19
NETWORK_DISCONNECT_STRINGTABLEMSG_OVERFLOW = 20
NETWORK_DISCONNECT_DELTAENTMSG_OVERFLOW = 21
NETWORK_DISCONNECT_TEMPENTMSG_OVERFLOW = 22
NETWORK_DISCONNECT_SOUNDSMSG_OVERFLOW = 23
NETWORK_DISCONNECT_SNAPSHOTOVERFLOW = 24
NETWORK_DISCONNECT_SNAPSHOTERROR = 25
NETWORK_DISCONNECT_RELIABLEOVERFLOW = 26
NETWORK_DISCONNECT_BADDELTATICK = 27
NETWORK_DISCONNECT_NOMORESPLITS = 28
NETWORK_DISCONNECT_TIMEDOUT = 29
NETWORK_DISCONNECT_DISCONNECTED = 30
NETWORK_DISCONNECT_LEAVINGSPLIT = 31
NETWORK_DISCONNECT_DIFFERENTCLASSTABLES = 32
NETWORK_DISCONNECT_BADRELAYPASSWORD = 33
NETWORK_DISCONNECT_BADSPECTATORPASSWORD = 34
NETWORK_DISCONNECT_HLTVRESTRICTED = 35
NETWORK_DISCONNECT_NOSPECTATORS = 36
NETWORK_DISCONNECT_HLTVUNAVAILABLE = 37
NETWORK_DISCONNECT_HLTVSTOP = 38
NETWORK_DISCONNECT_KICKED = 39
NETWORK_DISCONNECT_BANADDED = 40
NETWORK_DISCONNECT_KICKBANADDED = 41
NETWORK_DISCONNECT_HLTVDIRECT = 42
NETWORK_DISCONNECT_PURESERVER_CLIENTEXTRA = 43
NETWORK_DISCONNECT_PURESERVER_MISMATCH = 44
NETWORK_DISCONNECT_USERCMD = 45
NETWORK_DISCONNECT_REJECTED_BY_GAME = 46
NETWORK_DISCONNECT_MESSAGE_PARSE_ERROR = 47
NETWORK_DISCONNECT_INVALID_MESSAGE_ERROR = 48
NETWORK_DISCONNECT_BAD_SERVER_PASSWORD = 49
NETWORK_DISCONNECT_DIRECT_CONNECT_RESERVATION = 50
NETWORK_DISCONNECT_CONNECTION_FAILURE = 51
NETWORK_DISCONNECT_NO_PEER_GROUP_HANDLERS = 52
NETWORK_DISCONNECT_RECONNECTION = 53
NETWORK_DISCONNECT_CONNECTION_CLOSING = 54
NETWORK_DISCONNECT_NO_GOTV_RELAYS_AVAILABLE = 55
NETWORK_DISCONNECT_SESSION_MIGRATED = 56
NETWORK_DISCONNECT_VERYLARGETRANSFEROVERFLOW = 57
NETWORK_DISCONNECT_SENDNETOVERFLOW = 58
NETWORK_DISCONNECT_PLAYER_REMOVED_FROM_HOST_SESSION = 59

NETWORK_CONNECTION_TOKEN_FIELD_NUMBER = 50500
network_connection_token = _descriptor.FieldDescriptor(
  name='network_connection_token', full_name='network_connection_token', index=0,
  number=50500, type=9, cpp_type=9, label=1,
  has_default_value=False, default_value=_b("").decode('utf-8'),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR)

DESCRIPTOR.enum_types_by_name['ENetworkDisconnectionReason'] = _ENETWORKDISCONNECTIONREASON
DESCRIPTOR.extensions_by_name['network_connection_token'] = network_connection_token
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

google_dot_protobuf_dot_descriptor__pb2.EnumValueOptions.RegisterExtension(network_connection_token)

DESCRIPTOR._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_DISCONNECT_BY_USER"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_DISCONNECT_BY_SERVER"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_LOST"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_OVERFLOW"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_STEAM_BANNED"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_STEAM_INUSE"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_STEAM_TICKET"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_STEAM_LOGON"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_STEAM_AUTHCANCELLED"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_STEAM_AUTHALREADYUSED"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_STEAM_AUTHINVALID"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_STEAM_VACBANSTATE"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_STEAM_LOGGED_IN_ELSEWHERE"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_STEAM_VAC_CHECK_TIMEDOUT"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_STEAM_DROPPED"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_STEAM_OWNERSHIP"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_SERVERINFO_OVERFLOW"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_TICKMSG_OVERFLOW"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_STRINGTABLEMSG_OVERFLOW"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_DELTAENTMSG_OVERFLOW"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_TEMPENTMSG_OVERFLOW"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_SOUNDSMSG_OVERFLOW"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_SNAPSHOTOVERFLOW"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_SNAPSHOTERROR"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_RELIABLEOVERFLOW"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_BADDELTATICK"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_NOMORESPLITS"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_TIMEDOUT"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_DISCONNECTED"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_LEAVINGSPLIT"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_DIFFERENTCLASSTABLES"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_BADRELAYPASSWORD"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_BADSPECTATORPASSWORD"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_HLTVRESTRICTED"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_NOSPECTATORS"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_HLTVUNAVAILABLE"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_HLTVSTOP"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_KICKED"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_BANADDED"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_KICKBANADDED"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_HLTVDIRECT"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_PURESERVER_CLIENTEXTRA"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_PURESERVER_MISMATCH"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_USERCMD"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_REJECTED_BY_GAME"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_MESSAGE_PARSE_ERROR"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_INVALID_MESSAGE_ERROR"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_BAD_SERVER_PASSWORD"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_DIRECT_CONNECT_RESERVATION"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_CONNECTION_FAILURE"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_NO_PEER_GROUP_HANDLERS"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_RECONNECTION"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_CONNECTION_CLOSING"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_NO_GOTV_RELAYS_AVAILABLE"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_SESSION_MIGRATED"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_VERYLARGETRANSFEROVERFLOW"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_SENDNETOVERFLOW"]._options = None
_ENETWORKDISCONNECTIONREASON.values_by_name["NETWORK_DISCONNECT_PLAYER_REMOVED_FROM_HOST_SESSION"]._options = None
# @@protoc_insertion_point(module_scope)