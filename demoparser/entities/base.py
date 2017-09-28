class BaseEntity:

    def __init__(self, parser, index, class_id, serial, props):
        self.parser = parser
        self.index = index
        self.class_id = class_id
        self.serial = serial
        self.props = props

    def update_prop(self, table, key, value):
        self.props[table][key] = value

    def get_prop(self, table, var):
        return self.props[table][var]

    @property
    def position(self):
        return self.get_prop('DT_BaseEntity', 'm_vecOrigin')

    @property
    def server_class(self):
        return self.parser.server_classes[self.class_id]

    @property
    def team_num(self):
        return self.get_prop('DT_BaseEntity', 'm_iTeamNum')

    @property
    def team(self):
        team_num = self.team_num

        if not team_num:
            return

        return self.parser.entities.teams[team_num]

    @property
    def owner(self):
        return self.parser.entities.get_by_handle(
            self.get_prop('DT_BaseEntity', 'm_hOwnerEntity')
        )
