import inspect
from demoparser.entities import BaseEntity


class Team(BaseEntity):

    def __init__(self, parser, index, class_id, serial, props):
        self.parser = parser
        self.index = index
        self.class_id = class_id
        self.serial = serial
        self.props = props

    @property
    def tid(self):
        """Team id."""
        return self.get_prop('DT_Team', 'm_iTeamNum')
        
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
