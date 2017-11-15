from demoparser.entities import BaseEntity
import inspect


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
        users = self.parser.table_by_name('userinfo')['entries']
        return users[self.slot]['user_data']

    @property
    def health(self):
        """Get current health."""
        return self.get_prop('DT_BasePlayer', 'm_iHealth')

    @property
    def name(self):
        """Get player's name."""
        if isinstance(self.user_info, bytes):
            return ""
        return self.user_info.name.decode('utf-8')

    @property
    def steam_id(self):
        """Get Steam ID."""
        return self.user_info.guid.decode('utf-8')

    @property
    def position(self):
        """Get current position.

        :returns: Position vector.
        """
        vec = self.get_prop('DT_CSLocalPlayerExclusive', 'm_vecOrigin')
        z = self.get_prop('DT_CSLocalPlayerExclusive', 'm_vecOrigin[2]')

        return {
            'x': vec['x'],
            'y': vec['y'],
            'z': z
        }

    @property
    def view_angle(self):
        """Get current view angle.

        :returns: Tuple of pitch and yaw.
        """
        pitch = self.get_prop('DT_CSPlayer', 'm_angEyeAngles[0]')
        yaw = self.get_prop('DT_CSPlayer', 'm_angEyeAngles[1]')

        return {'pitch': pitch, 'yaw': yaw}

    @property
    def cash(self):
        """Get """
        return self.get_prop('DT_CSPlayer', 'm_iAccount')

    @property
    def life_state(self):
        """Get life state.

        0
          Alive.

        1
          Dying. Either the death animation is still playing
          or the player is falling and waiting to hit the ground.

        2
          Dead. Not moving.

        :returns: Life state.
        """
        return self.get_prop('DT_BasePlayer', 'm_lifeState')

    @property
    def armor(self):
        """Get armor value."""
        return self.get_prop('DT_CSPlayer', 'm_ArmorValue')

    @property
    def place(self):
        """Get last place player occupied.

        A place refers a named navigation mesh. A navigation mesh
        represents the walkable areas of a map.

        :returns: Name of last nav mesh occupied.
        """
        return self.get_prop('DT_BasePlayer', 'm_szLastPlaceName')

    @property
    def kills(self):
        """Number of kills for this player."""
        if isinstance(self.user_info, bytes):
            return 0
        prop = self.parser.entities.get_one('DT_CSPlayerResource')
        # This property has a list of kills for all players
        kills = prop.props['m_iKills']
        player_id = str(self.user_info.user_id).zfill(3)
        return kills[player_id]

    @property
    def weapon(self):
        """Get current weapon."""
        return self.parser.entities.get_by_handle(
            self.get_prop('DT_BaseCombatCharacter', 'm_hActiveWeapon')
        )

    def properties(self):
        result = {
            'index': self.index,
            'class_id': self.class_id,
            'serial': self.serial,
        }

        for name, value in inspect.getmembers(self):
            prop_attr = getattr(self.__class__, name, None)
            if inspect.isdatadescriptor(prop_attr):
                attr = getattr(self, name, None)
                if not isinstance(attr, BaseEntity):
                    result[name] = value

        return result
