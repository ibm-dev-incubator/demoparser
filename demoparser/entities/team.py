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
        """Team name. Either 'T' or 'CT'."""
        return self.get_prop('DT_Team', 'm_szTeamname')

    @property
    def clan(self):
        """Clan name."""
        return self.get_prop('DT_Team', 'm_szClanTeamname')

    @property
    def score(self):
        """Final team score."""
        return self.get_prop('DT_Team', 'm_scoreTotal')

    @property
    def score_first_half(self):
        """Score for first half of match."""
        return self.get_prop('DT_Team', 'm_scoreFirstHalf')

    @property
    def score_second_half(self):
        """Score for second half of match."""
        return self.get_prop('DT_Team', 'm_scoreSecondHalf')
