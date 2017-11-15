import inspect
from demoparser.entities import BaseEntity


class GameRules(BaseEntity):

    def __init__(self, parser, index, class_id, serial, props):
        self.parser = parser
        self.index = index
        self.class_id = class_id
        self.serial = serial
        self.props = props

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
