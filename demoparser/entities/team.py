from demoparser.entities import BaseEntity


class Team(BaseEntity):

    def __init__(self, parser, index, class_id, serial, props):
        self.parser = parser
        self.index = index
        self.class_id = class_id
        self.serial = serial
        self.props = props

    @property
    def name(self):
        return self.get_prop('DT_Team', 'm_szTeamname')

    @property
    def clan(self):
        return self.get_prop('DT_Team', 'm_szClanTeamname')

    @property
    def score(self):
        return self.get_prop('DT_Team', 'm_scoreTotal')

    @property
    def score_first_half(self):
        return self.get_prop('DT_Team', 'm_scoreFirstHalf')

    @property
    def score_second_half(self):
        return self.get_prop('DT_Team', 'm_scoreSecondHalf')
