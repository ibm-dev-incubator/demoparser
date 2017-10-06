# cython: profile=True
from demoparser.bitbuffer cimport Bitbuffer
from demoparser.bytebuffer import Bytebuffer
from libc cimport math

from collections import defaultdict
from collections import deque
from collections import OrderedDict

from demoparser import consts
from demoparser.protobufs import netmessages_pb2
from demoparser.protobufs import cstrike15_usermessages_pb2 as um
from demoparser.entities import EntityList
from demoparser.props cimport PropFlags
from demoparser.props cimport PropTypes
from demoparser.structures import UserInfo
from demoparser.structures import DemoHeader

from demoparser.util cimport parse_entity_update


cdef bint _key_sort(dict item):
    if item.get('collapsible', True) is False:
        return 0
    return 1


cdef enum DemoCommand:
    SIGNON = 1
    PACKET = 2
    SYNCTICK = 3
    CONSOLECMD = 4
    USERCMD = 5
    DATATABLES = 6
    STOP = 7
    CUSTOMDATA = 8
    STRINGTABLES = 9


cdef class DemoFile:

    cdef public unsigned int current_tick
    cdef list data_tables
    cdef list string_tables
    cdef list server_classes
    cdef object game_events
    cdef object pending_baselines
    cdef public object instance_baselines
    cdef public object entities
    cdef object callbacks
    cdef dict internal_callbacks
    cdef dict merged_enums
    cdef dict user_messages
    cdef unsigned int server_class_bits
    cdef object byte_buf
    cdef object header

    def __cinit__(self, bytes data):
        self.header = DemoHeader.from_data(data[:1072])
        self.byte_buf = Bytebuffer(data[1072:])

        self.merged_enums = {
            v[1]: v[0] for v in netmessages_pb2.NET_Messages.items() +
            netmessages_pb2.SVC_Messages.items()
        }
        self.user_messages = {
            v[1]: v[0] for v in um.ECstrike15UserMessages.items()
        }
        self.current_tick = 0
        self.data_tables = []
        self.string_tables = []
        self.server_classes = []
        self.game_events = OrderedDict()
        self.pending_baselines = OrderedDict()
        self.instance_baselines = OrderedDict()
        self.entities = EntityList(self)
        self.callbacks = defaultdict(list)
        self.internal_callbacks = {
            'svc_GameEventList': [self._handle_game_event_list],
            'svc_GameEvent': [self._handle_game_event],
            'svc_CreateStringTable': [self._create_string_table],
            'svc_UpdateStringTable': [self._update_string_table],
            'svc_PacketEntities': [self._handle_packet_entities],
            'svc_UserMessage': [self.handle_user_message],
            'string_table_update': [self._table_updated]
        }

    cdef void _fire_event(self, str event, args=None):
        if args is None:
            args = []

        for func in self.internal_callbacks.get(event, []):
            # cdef instance methods don't seem to include self
            # when called this way.
            func(self, *args)

        for func in self.callbacks.get(event, []):
            func(*args)

    cpdef add_callback(self, event, func):
        self.callbacks[event].append(func)

    cpdef void parse(self) except *:
        while True:
            header = self.byte_buf.read_command_header()
            if header.tick != self.current_tick:
                self._fire_event('tick_end', [self.current_tick])
                self.current_tick = header.tick
                self._fire_event('tick_start', [self.current_tick])

            if header.command in (DemoCommand.SIGNON, DemoCommand.PACKET):
                self._handle_demo_packet(header)
            elif header.command == DemoCommand.SYNCTICK:
                continue
            elif header.command == DemoCommand.CONSOLECMD:
                length, buf = self.byte_buf.read_raw_data()
            elif header.command == DemoCommand.USERCMD:
                self.byte_buf.read_user_command()
            elif header.command == DemoCommand.DATATABLES:
                self._handle_data_table(header)
            elif header.command == DemoCommand.CUSTOMDATA:
                pass
            elif header.command == DemoCommand.STRINGTABLES:
                self._handle_string_tables(header)
            elif header.command == DemoCommand.STOP:
                self._fire_event('tick_end', [self.current_tick])
                self._fire_event('end')
                break
            else:
                raise Exception("Unrecognized command")

    cdef void handle_user_message(self, object msg):
        um_class = self.user_messages[msg.msg_type]
        class_name = 'CCSUsrMsg_{}'.format(um_class[6:])

        user_message = getattr(um, class_name)()
        user_message.ParseFromString(msg.msg_data)

        self._fire_event(um_class[6:], [user_message])

    cdef void _handle_packet_entities(self, object msg):
        cdef unsigned int i = 0
        cdef int entity_idx = -1
        cdef Bitbuffer buf = Bitbuffer(msg.entity_data)

        for i in range(msg.updated_entries):
            entity_idx += 1 + buf.read_var_int()

            if buf.read_bit():
                if buf.read_bit():
                    self.entities[entity_idx] = None
            elif buf.read_bit():
                class_id = buf.read_uint_bits(self.server_class_bits)
                serial = buf.read_uint_bits(
                    consts.NUM_NETWORKED_EHANDLE_SERIAL_NUMBER_BITS
                )

                new_entity = self.entities.new_entity(
                    entity_idx, class_id, serial
                )
                self._read_new_entity(buf, new_entity)
            else:
                entity = self.entities[entity_idx]
                self._read_new_entity(buf, entity)

    cdef void _read_new_entity(self, Bitbuffer buf, object entity):
        cdef object server_class = self.server_classes[entity.class_id]
        cdef list updates = parse_entity_update(buf, server_class)

        for update in updates:
            table_name = update['prop']['table'].net_table_name
            var_name = update['prop']['prop'].var_name

            self._fire_event(
                'change', [entity, table_name, var_name, update['value']]
            )
            entity.update_prop(table_name, var_name, update['value'])

    cdef void _handle_demo_packet(self, cmd_header):

        self.byte_buf.read_command_data()
        self.byte_buf.read_sequence_data()

        for cmd, size, data in self.byte_buf.read_packet_data():
            cls = self._class_by_net_message_type(cmd)()

            cls.ParseFromString(data)
            self._fire_event(self.merged_enums[cmd], [cls])

    cdef void _handle_data_table(self, cmd_header) except *:
        cdef unsigned int i = 0
        # Size of entire data table chunk
        self.byte_buf.read(4)
        table = self._class_by_message_name('svc_SendTable')

        while True:
            # Type of table, not needed for now
            self.byte_buf.read_varint()

            data = self.byte_buf.read_var_bytes()

            msg = table()
            msg.ParseFromString(data)
            if msg.is_end:
                break

            self.data_tables.append(msg)

        server_classes = self.byte_buf.read_short()
        self.server_class_bits = <unsigned int>math.ceil(
            math.log2(server_classes)
        )

        for i in range(server_classes):
            class_id = self.byte_buf.read_short()
            assert class_id == i

            name = self.byte_buf.read_string()
            table_name = self.byte_buf.read_string()

            dt = self._data_table_by_name(table_name)

            table = {
                'class_id': class_id,
                'name': name,
                'table_name': table_name,
                'props': self._flatten_data_table(dt)
            }
            self.server_classes.append(table)

            # Handle pending baselines
            pending_baseline = self.pending_baselines.get(class_id)
            if pending_baseline:
                self.instance_baselines[class_id] = \
                    self._parse_instance_baseline(
                        pending_baseline, class_id
                )
                self._fire_event(
                    'baseline_update',
                    [class_id,
                     table,
                     self.instance_baselines[class_id]]
                )
                del self.pending_baselines[class_id]

        self._fire_event('datatable_ready', [table])

    cdef void _update_string_table(self, object msg):
        buf = Bitbuffer(msg.string_data)

        table = self.string_tables[msg.table_id]

        self._parse_string_table_update(
            buf, table, msg.num_changed_entries, len(table['entries']),
            0, False
        )

    cdef void _create_string_table(self, object msg):
        cdef Bitbuffer buf = Bitbuffer(msg.string_data)

        table = {
            'name': msg.name,
            'entries': [{'entry': None, 'user_data': None}] * msg.max_entries
        }
        self.string_tables.append(table)
        self._parse_string_table_update(
            buf, table, msg.num_entries, msg.max_entries,
            msg.user_data_size_bits, msg.user_data_fixed_size
        )

    cdef void _parse_string_table_update(
            self, Bitbuffer buf, object table, unsigned int num_entries,
            unsigned int max_entries, unsigned int user_data_bits,
            bint user_data_fixed_size):
        cdef unsigned int entry_bits = <unsigned int>math.log2(max_entries)
        cdef unsigned int i = 0
        history = deque(maxlen=32)

        dict_encode = buf.read_bit()
        assert not dict_encode, 'Dictionary encoding not supported'

        for i in range(num_entries):
            index = i
            entry = None

            if not buf.read_bit():
                index = buf.read_uint_bits(entry_bits)

            assert index >=0 and index <= max_entries

            # entry changed?
            changed = buf.read_bit()
            if changed:
                # substring check
                substr = buf.read_bit()
                if substr:
                    idx = buf.read_uint_bits(5)
                    bytes_to_copy = buf.read_uint_bits(consts.SUBSTRING_BITS)
                    substring = history[idx][:bytes_to_copy * 8]
                    suffix = buf.read_string()
                    entry = substring + suffix
                else:
                    entry = buf.read_string()

                table['entries'][index]['entry'] = entry

            # Deal with user data
            user_data = None
            if buf.read_bit():
                if user_data_fixed_size:
                    user_data = buf.read_user_data(user_data_bits)
                else:
                    size = buf.read_uint_bits(consts.MAX_USERDATA_BITS)
                    user_data = buf.read_user_data(size * 8)

                if table['name'] == 'userinfo':
                    user_data = UserInfo.from_data(user_data)

                table['entries'][index]['user_data'] = user_data

            history.append(entry)
            self._fire_event(
                'string_table_update', [table, index, entry, user_data]
            )

    cdef void _handle_string_tables(self, object cmd_header):
        cdef Bitbuffer buf = self.byte_buf.read_bitstream()
        cdef unsigned char num_tables = buf.read_uint_bits(8)
        cdef unsigned char i = 0

        for i in range(num_tables):
            table_name = buf.read_string()
            self._handle_string_table(table_name, buf)

    cdef void _handle_string_table(self, str table_name, Bitbuffer buf):
        cdef unsigned short entries = buf.read_uint_bits(16)
        cdef unsigned short entry_idx = 0
        table = self._table_by_name(table_name)

        for entry_idx in range(entries):
            entry_name = buf.read_string()

            one_bit = buf.read_bit()
            user_data = None
            if one_bit:
                user_data_len = buf.read_uint_bits(16)
                user_data = buf.read_user_data(user_data_len * 8)
                if table_name == 'userinfo':
                    user_data = UserInfo.from_data(user_data)

            table['entries'][entry_idx] = {
                'entry': entry_name,
                'user_data': user_data
            }

            self._fire_event(
                'string_table_update',
                [table, entry_idx, entry_name, user_data]
            )

        # Client-side entries, maybe they don't exist? I've never seen them
        if buf.read_bit():
            num_strings = buf.read_uint_bits(16)

            for string in range(num_strings):
                # entry name
                buf.read_string()
                user_data = None

                if buf.read_bit():
                    user_data_len = buf.read_uint_bits(16)
                    user_data = buf.read_user_data(user_data_len * 8)

    cdef void _handle_game_event_list(self, object msg):
        for event in msg.descriptors:
            self.game_events.update({
                event.eventid: {
                    'name': event.name,
                    'event': event
                }
            })

    cdef void _handle_game_event(self, object msg):
        event = self.game_events[msg.eventid]
        self._fire_event(event['name'], [event, msg])

    cdef object _class_by_net_message_type(self, unsigned int msg_type):
        cls = self.merged_enums[msg_type]

        if not cls:
            raise Exception(
                "Class for message type {} not found.".format(msg_type)
            )

        enum_type = cls[:3]
        enum_name = cls[4:]
        class_name = 'C{}Msg_{}'.format(enum_type.upper(), enum_name)

        return getattr(netmessages_pb2, class_name)

    cdef object _class_by_message_name(self, str name):
        enum_type = name[:3]
        enum_name = name[4:]
        class_name = 'C{}Msg_{}'.format(enum_type.upper(), enum_name)
        return getattr(netmessages_pb2, class_name)

    cpdef object _table_by_name(self, str name):
        return [t for t in self.string_tables if t['name'] == name][0]

    cdef object _data_table_by_name(self, str name):
        return [t for t in self.data_tables if t.net_table_name == name][0]

    cdef void _table_updated(self, table, index, entry, user_data):
        if table['name'] != 'instancebaseline' or not user_data:
            return

        cdef unsigned int class_id = int(entry)
        cdef Bitbuffer baseline_buf = Bitbuffer(user_data)

        try:
            self.server_classes[class_id]
        except IndexError:
            self.pending_baselines[class_id] = baseline_buf
            return

        self.instance_baselines[class_id] = self._parse_instance_baseline(
            baseline_buf, class_id
        )

    cdef object _parse_instance_baseline(self, Bitbuffer buf,
                                         unsigned int class_id):
        class_baseline = OrderedDict()
        server_class = self.server_classes[class_id]

        for baseline in parse_entity_update(buf, server_class):
            table_name = baseline['prop']['table'].net_table_name
            var_name = baseline['prop']['prop'].var_name

            if table_name not in class_baseline:
                class_baseline[table_name] = OrderedDict()
            class_baseline[table_name][var_name] = baseline['value']

        return class_baseline

    cdef object _flatten_data_table(self, table):
        flattened_props = self._collect_props(
            table, self._collect_exclusions(table)
        )

        priorities = set(p['prop'].priority for p in flattened_props)
        priorities.add(64)
        priorities = sorted(list(priorities))

        start = 0
        for prio in priorities:
            while True:
                current_prop = start
                while current_prop < len(flattened_props):
                    prop = flattened_props[current_prop]['prop']
                    if (prop.priority == prio or (prio == 64 and
                       (prop.flags & PropFlags.SPROP_CHANGES_OFTEN))):
                        if start != current_prop:
                            temp = flattened_props[start]
                            flattened_props[start] = \
                                flattened_props[current_prop]
                            flattened_props[current_prop] = temp
                        start += 1
                        break
                    current_prop += 1
                if current_prop == len(flattened_props):
                    break

        # Doesn't seem to work
        # props = sorted(flattened_props, key=lambda x: x['prop'].priority)
        return flattened_props

    cdef bint _is_prop_excluded(self, list exclusions,
                                object table, object prop):
        for exclusion in exclusions:
            if (table.net_table_name == exclusion.dt_name and
               prop.var_name == exclusion.var_name):
                return True

    cdef list _collect_exclusions(self, object table):
        exclusions = []
        cdef unsigned int idx

        for idx, prop in enumerate(table.props):
            if prop.flags & PropFlags.SPROP_EXCLUDE:
                exclusions.append(prop)

            if prop.type == PropTypes.DPT_DataTable:
                sub_table = self._data_table_by_name(prop.dt_name)
                exclusions.extend(self._collect_exclusions(sub_table))
        return exclusions

    cdef list _collect_props(self, object table, list exclusions):
        flattened = []
        cdef unsigned int idx

        for idx, prop in enumerate(table.props):

            if (prop.flags & PropFlags.SPROP_INSIDEARRAY or
               prop.flags & PropFlags.SPROP_EXCLUDE or
               self._is_prop_excluded(exclusions, table, prop)):
                continue

            if prop.type == PropTypes.DPT_DataTable:
                sub_table = self._data_table_by_name(prop.dt_name)
                child_props = self._collect_props(sub_table, exclusions)

                if prop.flags & PropFlags.SPROP_COLLAPSIBLE == 0:
                    for cp in child_props:
                        cp['collapsible'] = False

                flattened.extend(child_props)
            elif prop.type == PropTypes.DPT_Array:
                flattened.append({
                    'prop': prop,
                    'array_element_prop': table.props[idx - 1],
                    'table': table
                })
            else:
                flattened.append({
                    'prop': prop,
                    'table': table
                })

        return sorted(flattened, key=_key_sort)
