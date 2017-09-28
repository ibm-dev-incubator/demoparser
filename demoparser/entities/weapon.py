from demoparser.entities import BaseEntity


class Weapon(BaseEntity):

    def __init__(self, parser, index, class_id, serial, props):
        self.parser = parser
        self.index = index
        self.class_id = class_id
        self.serial = serial
        self.props = props

    @property
    def item_index(self):
        return self.get_prop('DT_ScriptCreatedItem', 'm_iItemDefinitionIndex')

    @property
    def name(self):
        return

    @property
    def previous_owner(self):
        handle = self.get_prop('DT_WeaponCSBase', 'm_hPrevOwner')
        return self.parser.entities.get_by_handle(handle)
