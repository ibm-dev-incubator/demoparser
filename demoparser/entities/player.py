from demoparser.entities import BaseEntity


class Player(BaseEntity):

    def __init__(self, parser, index, class_id, serial, props):
        self.parser = parser
        self.index = index
        self.slot = self.index - 1
        self.class_id = class_id
        self.serial = serial
        self.props = props
        self.user_info = self._get_user_info()
        self._serialize_props = [

        ]

    def _get_user_info(self):
        users = self.parser._table_by_name('userinfo')['entries']
        return users[self.slot]['user_data']

    @property
    def health(self):
        return self.get_prop('DT_BasePlayer', 'm_iHealth')

    @property
    def name(self):
        if isinstance(self.user_info, bytes):
            print(len(self.user_info), self.user_info)
            return ""
        return self.user_info.name

    @property
    def steam_id(self):
        return self.user_info.guid

    @property
    def position(self):
        vec = self.get_prop('DT_CSLocalPlayerExclusive', 'm_vecOrigin')
        z = self.get_prop('DT_CSLocalPlayerExclusive', 'm_vecOrigin[2]')

        return {
            'x': vec['x'],
            'y': vec['y'],
            'z': z
        }

    @property
    def view_angle(self):
        pitch = self.get_prop('DT_CSPlayer', 'm_angEyeAngles[0]')
        yaw = self.get_prop('DT_CSPlayer', 'm_angEyeAngles[1]')

        return {'pitch': pitch, 'yaw': yaw}

    @property
    def cash(self):
        return self.get_prop('DT_CSPlayer', 'm_iAccount')

    @property
    def life_state(self):
        return self.get_prop('DT_BasePlayer', 'm_lifeState')

    @property
    def armor(self):
        return self.get_prop('DT_CSPlayer', 'm_ArmorValue')

    @property
    def place(self):
        return self.get_prop('DT_BasePlayer', 'm_szLastPlaceName')

    @property
    def kills(self):
        if isinstance(self.user_info, bytes):
            return 0
        prop = self.parser.entities.get_one('DT_CSPlayerResource')
        # This property has a list of kills for all players
        kills = prop.props['m_iKills']
        player_id = str(self.user_info.user_id).zfill(3)
        return kills[player_id]

    @property
    def weapon(self):
        return self.parser.entities.get_by_handle(
            self.get_prop('DT_BaseCombatCharacter', 'm_hActiveWeapon')
        )

    def serialize(self, props=None):
        props = props or self._serialize_props
