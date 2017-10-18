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
        self.callbacks.update({
            'svc_GameEventList': [self.handle_game_event_list],
            'svc_GameEvent': [self.handle_game_event],
            'svc_CreateStringTable': [self.create_string_table],
            'svc_UpdateStringTable': [self.update_string_table],
            'svc_PacketEntities': [self.handle_packet_entities],
            'svc_UserMessage': [self.handle_user_message],
            'string_table_update': [self.table_updated]
        })

    cpdef void emit(self, str event, args=None):
        """Run callback functions for an event.

        Each time an event is trigged each registered callback
        will be called with the arguments provided to this method.

        A separate set of internal callbacks is maintained because
        they require a different calling method. Internal callbacks
        are callbacks functions that belong to a DemoFile instance.
        """
        if args is None:
            args = []

        for func in self.callbacks.get(event, []):
            func(*args)

    cpdef add_callback(self, event, func):
        """Register a callback function for an event."""
        self.callbacks[event].append(func)

    cpdef void parse(self) except *:
        """Parse the demofile.

        :emits: :ref:`tick_start <event_tick_start>`, \
                :ref:`tick_end <event_tick_end>`, \
                :ref:`end <event_end>`
        """
        while True:
            header = self.byte_buf.read_command_header()
            if header.tick != self.current_tick:
                self.emit('tick_end', [self.current_tick])
                self.current_tick = header.tick
                self.emit('tick_start', [self.current_tick])

            if header.command in (DemoCommand.SIGNON, DemoCommand.PACKET):
                self.handle_demo_packet(header)
            elif header.command == DemoCommand.SYNCTICK:
                continue
            elif header.command == DemoCommand.CONSOLECMD:
                length, buf = self.byte_buf.read_raw_data()
            elif header.command == DemoCommand.USERCMD:
                self.byte_buf.read_user_command()
            elif header.command == DemoCommand.DATATABLES:
                self.handle_data_table(header)
            elif header.command == DemoCommand.CUSTOMDATA:
                pass
            elif header.command == DemoCommand.STRINGTABLES:
                self.handle_string_tables(header)
            elif header.command == DemoCommand.STOP:
                self.emit('tick_end', [self.current_tick])
                self.emit('end')
                break
            else:
                raise Exception("Unrecognized command")

    cpdef void handle_user_message(self, object msg):
        """Handle user message.

        A user message is stuff like text chat,
        voice chat, radio messages, etc.

        :emits: :ref:`user_message <event_user_msg>`
        """
        um_class = self.user_messages[msg.msg_type]
        class_name = 'CCSUsrMsg_{}'.format(um_class[6:])

        user_message = getattr(um, class_name)()
        user_message.ParseFromString(msg.msg_data)

        self.emit(um_class[6:], [user_message])

    cpdef void handle_packet_entities(self, object msg):
        """Create or update an entity.

        Entities represent in-game objects and are networked (i.e.
        their state is maintained on the server and updates are sent
        to one or more clients).

        Entities have a class ID which defines the type of entity
        it is. The class ID is also used to find the correct
        instance baseline. Instance baselines serve as default
        values when entities are created.
        """
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
                self.read_new_entity(buf, new_entity)
            else:
                entity = self.entities[entity_idx]
                self.read_new_entity(buf, entity)

    cpdef void read_new_entity(self, Bitbuffer buf, object entity):
        """Read entity data.

        A list of updates is computed and for each one of those
        the appropritate property of the entity instance is updated.

        :emits: :ref:`change <event_change>`
        """
        cdef object server_class = self.server_classes[entity.class_id]
        cdef list updates = parse_entity_update(buf, server_class)

        for update in updates:
            table_name = update['prop']['table'].net_table_name
            var_name = update['prop']['prop'].var_name

            self.emit(
                'change', [entity, table_name, var_name, update['value']]
            )
            entity.update_prop(table_name, var_name, update['value'])

    cpdef void handle_demo_packet(self, cmd_header):
        """Handle demo packet.

        Demo packets are of type SVC\_ or NET\_. This method
        instantiates the appropriate protobuf class and triggers
        an event.

        :emits: :ref:`demo_packet <event_demo_packet>`.
        """
        self.byte_buf.read_command_data()
        self.byte_buf.read_sequence_data()

        for cmd, size, data in self.byte_buf.read_packet_data():
            cls = self.class_by_net_message_type(cmd)()

            cls.ParseFromString(data)
            self.emit(self.merged_enums[cmd], [cls])

    cpdef void handle_data_table(self, cmd_header):
        """Create data tables.

        Each entity class maintains a data table that describes
        how to encode each of its properties. These tables are
        called Send Tables and and genrally have names like
        DT_EntityClassName (DT_CSPlayer, DT_Weapon, etc.)

        :emits: :ref:`baseline_create <event_baseline_create>`, \
                :ref:`datatable_ready <event_datatable_ready>`.
        """
        cdef unsigned int i = 0
        # Size of entire data table chunk
        self.byte_buf.read(4)
        table = self.class_by_message_name('svc_SendTable')

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

            dt = self.data_table_by_name(table_name)

            table = {
                'class_id': class_id,
                'name': name,
                'table_name': table_name,
                'props': self.flatten_data_table(dt)
            }
            self.server_classes.append(table)

            # Handle pending baselines
            pending_baseline = self.pending_baselines.get(class_id)
            if pending_baseline:
                self.instance_baselines[class_id] = \
                    self.parse_instance_baseline(
                        pending_baseline, class_id
                )
                self.emit(
                    'baseline_created',
                    [class_id,
                     table,
                     self.instance_baselines[class_id]]
                )
                del self.pending_baselines[class_id]

        self.emit('datatable_ready', [table])

    cpdef void update_string_table(self, object msg):
        buf = Bitbuffer(msg.string_data)

        table = self.string_tables[msg.table_id]

        self.parse_string_table_update(
            buf, table, msg.num_changed_entries, len(table['entries']),
            0, False
        )

    cpdef void create_string_table(self, object msg):
        """Create a string table.

        A string table consists of a name and a list of entries.
        The maximum number of entries is created and initialized
        to None. This is done because future messages that update
        or reference string table entries do so by index.

        Each entry is a dictionary with two keys, entry and user_data.
        Entry is the name of the entry and user_data contains binary
        data related to the entry. In the 'user_info' string table
        user_data describes a UserInfo object.
        """
        cdef Bitbuffer buf = Bitbuffer(msg.string_data)

        table = {
            'name': msg.name,
            'entries': [{'entry': None, 'user_data': None}] * msg.max_entries
        }
        self.string_tables.append(table)
        self.parse_string_table_update(
            buf, table, msg.num_entries, msg.max_entries,
            msg.user_data_size_bits, msg.user_data_fixed_size
        )

    cpdef void parse_string_table_update(
            self, Bitbuffer buf, object table, unsigned int num_entries,
            unsigned int max_entries, unsigned int user_data_bits,
            bint user_data_fixed_size):
        """Update a string table.

        A single update message can update multiple table entries.
        Both the entry name and the user data can be updated.

        :emits: :ref:`string_table_update <event_string_table_update>`.
        """
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
            self.emit(
                'string_table_update', [table, index, entry, user_data]
            )

    cpdef void handle_string_tables(self, object cmd_header):
        cdef Bitbuffer buf = self.byte_buf.read_bitstream()
        cdef unsigned char num_tables = buf.read_uint_bits(8)
        cdef unsigned char i = 0

        for i in range(num_tables):
            table_name = buf.read_string()
            self.handle_string_table(table_name, buf)

    cpdef void handle_string_table(self, str table_name, Bitbuffer buf):
        """Populate a string table.

        :emits: :ref:`string_table_update <event_string_table_update>`.
        """
        cdef unsigned short entries = buf.read_uint_bits(16)
        cdef unsigned short entry_idx = 0
        table = self.table_by_name(table_name)

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

            self.emit(
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

    cpdef void handle_game_event_list(self, object msg):
        """Create game event list.

        This message contains a list of game events present in
        this replay. Later, when a game event occurs its ID can
        be used to get a game event object.
        """
        for event in msg.descriptors:
            self.game_events.update({
                event.eventid: {
                    'name': event.name,
                    'event': event
                }
            })

    cpdef void handle_game_event(self, object msg):
        """Handle game event.

        A game event message just contains an event ID.
        The corresponding event can be found in self.game_events.
        An event is then triggered for the game event itself.

        :emits: :ref:`game_event <event_game_event>`.
        """
        event = self.game_events[msg.eventid]
        self.emit(event['name'], [event, msg])

    cdef object class_by_net_message_type(self, unsigned int msg_type):
        """Find a Protobuf class for the given message type.

        The name for the message type is found and then converted
        to the Protobuf class naming convention.

        :returns: Protobuf class
        """
        cls = self.merged_enums[msg_type]

        if not cls:
            raise Exception(
                "Class for message type {} not found.".format(msg_type)
            )

        enum_type = cls[:3]
        enum_name = cls[4:]
        class_name = 'C{}Msg_{}'.format(enum_type.upper(), enum_name)

        return getattr(netmessages_pb2, class_name)

    cpdef object class_by_message_name(self, str name):
        """Find a Protobuf class for the given message.

        The generated Protobuf modules create classes like
        C<type>Msg_<name>. For a given message name this
        method will convert the name to a Protobuf class name
        and return it.

        :returns: Protobuf class
        """
        enum_type = name[:3]
        enum_name = name[4:]
        class_name = 'C{}Msg_{}'.format(enum_type.upper(), enum_name)
        return getattr(netmessages_pb2, class_name)

    cpdef object table_by_name(self, str name):
        return [t for t in self.string_tables if t['name'] == name][0]

    cpdef object data_table_by_name(self, str name):
        return [t for t in self.data_tables if t.net_table_name == name][0]

    cpdef void table_updated(self, table, index, entry, user_data):
        """Update an instance baseline.

        Each time a string table is updated this method is
        called. If a baseline doesn't exist yet it is added to
        the list of pending baselines which are handled later
        when the correct server class is created. Server classes
        are created by DATATABLES commands.
        """
        if table['name'] != 'instancebaseline' or not user_data:
            return

        cdef unsigned int class_id = int(entry)
        cdef Bitbuffer baseline_buf = Bitbuffer(user_data)

        try:
            self.server_classes[class_id]
        except IndexError:
            self.pending_baselines[class_id] = baseline_buf
            return

        self.instance_baselines[class_id] = self.parse_instance_baseline(
            baseline_buf, class_id
        )

    cpdef object parse_instance_baseline(self, Bitbuffer buf,
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

    cpdef object flatten_data_table(self, table):
        """Flatten a data table.

        Data tables can contain other data tables as entries.
        This method collects all properties and sorts them
        by priority.

        :returns: Flattened data table
        """
        flattened_props = self.collect_props(
            table, self.collect_exclusions(table)
        )

        priorities = set([p['prop'].priority for p in flattened_props])
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

    cpdef list collect_exclusions(self, object table):
        exclusions = []
        cdef unsigned int idx

        for idx, prop in enumerate(table.props):
            if prop.flags & PropFlags.SPROP_EXCLUDE:
                exclusions.append(prop)

            if prop.type == PropTypes.DPT_DataTable:
                sub_table = self.data_table_by_name(prop.dt_name)
                exclusions.extend(self.collect_exclusions(sub_table))
        return exclusions

    cpdef list collect_props(self, object table, list exclusions):
        """Collect table properties which are not excluded.

        If a property is part of an array or is flagged as
        excluded it will not be returned. Otherwise all
        properties are collected and data table entries are
        recursively collected.

        :returns: Flat list of all table properties
        """
        flattened = []
        cdef unsigned int idx

        for idx, prop in enumerate(table.props):

            if (prop.flags & PropFlags.SPROP_INSIDEARRAY or
               prop.flags & PropFlags.SPROP_EXCLUDE or
               self._is_prop_excluded(exclusions, table, prop)):
                continue

            if prop.type == PropTypes.DPT_DataTable:
                sub_table = self.data_table_by_name(prop.dt_name)
                child_props = self.collect_props(sub_table, exclusions)

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
