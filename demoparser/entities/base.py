class BaseEntity:

    def __init__(self, parser, index, class_id, serial, props):
        self.parser = parser
        self.index = index
        self.class_id = class_id
        self.serial = serial
        self.props = props

    def update_prop(self, table, key, value):
        """Update entity property."""
        self.props[table][key] = value

    def get_prop(self, table, var):
        return self.props[table][var]

    @property
    def position(self):
        """Get the position of this entity."""
        return self.get_prop('DT_BaseEntity', 'm_vecOrigin')

    @property
    def server_class(self):
        """Server class to which this entity belongs."""
        return self.parser.server_classes[self.class_id]

    @property
    def team_num(self):
        """Entity team number.

        :returns: Team number of entity.
        """
        return self.get_prop('DT_BaseEntity', 'm_iTeamNum')

    @property
    def team(self):
        """Team to which entity belongs.

        :returns: Team entity
        """
        team_num = self.team_num

        if not team_num:
            return

        return self.parser.entities.teams[team_num]

    @property
    def owner(self):
        """Find entity which owns this entity.

        For example, a weapon entity belongs to a player entity.
        Calling this method on a weapon entity would return a
        player.

        :returns: Owning entity.
        """
        return self.parser.entities.get_by_handle(
            self.get_prop('DT_BaseEntity', 'm_hOwnerEntity')
        )
