from enum import Enum
import inspect

from demoparser.entities import BaseEntity


class WeaponClass(Enum):
    PISTOL = 1
    RIFLE = 2
    SMG = 3
    SNIPER = 4
    MACHINE_GUN = 5
    SHOTGUN = 6
    KNIFE = 7
    GRENADE = 8
    GEAR = 9


# As found at:
# unknowncheats.me/wiki/Counter_Strike_Global_Offensive:Economy_Weapon_IDs
weapon_ids = {
    1: {
        'name': 'Desert Eagle',
        'class': WeaponClass.PISTOL,
        'ent_class': 'weapon_deagle'
    },
    2: {
        'name': 'Dual Berettas',
        'class': WeaponClass.PISTOL,
        'ent_class': 'weapon_elite'
    },
    3: {
        'name': 'Five-SeveN',
        'class': WeaponClass.PISTOL,
        'ent_class': 'weapon_fiveseven'
    },
    4: {
        'name': 'Glock-18',
        'class': WeaponClass.PISTOL,
        'ent_class': 'weapon_glock'
    },
    7: {
        'name': 'AK-47',
        'class': WeaponClass.RIFLE,
        'ent_class': 'weapon_ak47'
    },
    8: {
        'name': 'AUG',
        'class': WeaponClass.RIFLE,
        'ent_class': 'weapon_aug'
    },
    9: {
        'name': 'AWP',
        'class': WeaponClass.SNIPER,
        'ent_class': 'weapon_awp'
    },
    10: {
        'name': 'FAMAS',
        'class': WeaponClass.RIFLE,
        'ent_class': 'weapon_famas'
    },
    11: {
        'name': 'G3SG1',
        'class': WeaponClass.SNIPER,
        'ent_class': 'weapon_g3sg1'
    },
    13: {
        'name': 'Galil AR',
        'class': WeaponClass.RIFLE,
        'ent_class': 'weapon_galilar'
    },
    14: {
        'name': 'M249',
        'class': WeaponClass.MACHINE_GUN,
        'ent_class': 'weapon_m249'
    },
    16: {
        'name': 'M4A4',
        'class': WeaponClass.RIFLE,
        'ent_class': 'weapon_m4a1'
    },
    17: {
        'name': 'MAC-10',
        'class': WeaponClass.SMG,
        'ent_class': 'weapon_mac10'
    },
    19: {
        'name': 'P90',
        'class': WeaponClass.SMG,
        'ent_class': 'weapon_p90'
    },
    24: {
        'name': 'UMP-45',
        'class': WeaponClass.SMG,
        'ent_class': 'weapon_ump45'
    },
    25: {
        'name': 'XM1014',
        'class': WeaponClass.SHOTGUN,
        'ent_class': 'weapon_xm1014'
    },
    26: {
        'name': 'PP-Bizon',
        'class': WeaponClass.SMG,
        'ent_class': 'weapon_bizon'
    },
    27: {
        'name': 'MAG-7',
        'class': WeaponClass.SHOTGUN,
        'ent_class': 'weapon_mag7'
    },
    28: {
        'name': 'Negev',
        'class': WeaponClass.MACHINE_GUN,
        'ent_class': 'weapon_negev'
    },
    29: {
        'name': 'Sawed-off Shotgun',
        'class': WeaponClass.SHOTGUN,
        'ent_class': 'weapon_sawedoff'
    },
    30: {
        'name': 'Tec-9',
        'class': WeaponClass.PISTOL,
        'ent_class': 'weapon_tec9'
    },
    31: {
        'name': 'Zeus x27',
        'class': WeaponClass.GEAR,
        'ent_class': 'weapon_taser'
    },
    32: {
        'name': 'P2000',
        'class': WeaponClass.PISTOL,
        'ent_class': 'weapon_hkp2000'
    },
    33: {
        'name': 'MP7',
        'class': WeaponClass.SMG,
        'ent_class': 'weapon_mp7'
    },
    34: {
        'name': 'MP9',
        'class': WeaponClass.SMG,
        'ent_class': 'weapon_mp9'
    },
    35: {
        'name': 'Nova',
        'class': WeaponClass.SHOTGUN,
        'ent_class': 'weapon_nova'
    },
    36: {
        'name': 'P250',
        'class': WeaponClass.PISTOL,
        'ent_class': 'weapon_p250'
    },
    38: {
        'name': 'SCAR-20',
        'class': WeaponClass.SNIPER,
        'ent_class': 'weapon_scar20'
    },
    39: {
        'name': 'SG 553',
        'class': WeaponClass.RIFLE,
        'ent_class': 'weapon_sg556'
    },
    40: {
        'name': 'SSG 08',
        'class': WeaponClass.SNIPER,
        'ent_class': 'weapon_ssg08'
    },
    42: {
        'name': 'Knife',
        'class': WeaponClass.KNIFE,
        'ent_class': 'weapon_knife'
    },
    43: {
        'name': 'Flashbang',
        'class': WeaponClass.GRENADE,
        'ent_class': 'weapon_flashbang'
    },
    44: {
        'name': 'HE Grenade',
        'class': WeaponClass.GRENADE,
        'ent_class': 'weapon_hegrenade'
    },
    45: {
        'name': 'Smoke Grenade',
        'class': WeaponClass.GRENADE,
        'ent_class': 'weapon_smokegrenade'
    },
    46: {
        'name': 'Molotov',
        'class': WeaponClass.GRENADE,
        'ent_class': 'weapon_molotov'
    },
    47: {
        'name': 'Decoy Grenade',
        'class': WeaponClass.GRENADE,
        'ent_class': 'weapon_decoy'
    },
    48: {
        'name': 'Incendiary Grenade',
        'class': WeaponClass.GRENADE,
        'ent_class': 'weapon_incgrenade'
    },
    49: {
        'name': 'C4 Explosive',
        'class': WeaponClass.GEAR,
        'ent_class': 'weapon_c4'
    },
    59: {
        'name': 'Knife',
        'class': WeaponClass.KNIFE,
        'ent_class': 'weapon_knife_t'
    },
    60: {
        'name': 'M4A1-S',
        'class': WeaponClass.RIFLE,
        'ent_class': 'weapon_m4a1_silencer'
    },
    61: {
        'name': 'USP-S',
        'class': WeaponClass.PISTOL,
        'ent_class': 'weapon_usp_silencer'
    },
    63: {
        'name': 'CZ75 Auto',
        'class': WeaponClass.PISTOL,
        'ent_class': 'weapon_cz75a'
    },
    64: {
        'name': 'R8 Revolver',
        'class': WeaponClass.PISTOL,
        'ent_class': 'weapon_revolver'
    },
    500: {
        'name': 'Bayonet',
        'class': WeaponClass.KNIFE,
        'ent_class': 'weapon_bayonet'
    },
    505: {
        'name': 'Flip Knife',
        'class': WeaponClass.KNIFE,
        'ent_class': 'weapon_knife_flip'
    },
    506: {
        'name': 'Gut Knife',
        'class': WeaponClass.KNIFE,
        'ent_class': 'weapon_knife_gut'
    },
    507: {
        'name': 'Karambit',
        'class': WeaponClass.KNIFE,
        'ent_class': 'weapon_knife_karambit'
    },
    508: {
        'name': 'M9 Bayonet',
        'class': WeaponClass.KNIFE,
        'ent_class': 'weapon_knife_m9_bayonet'
    },
    509: {
        'name': 'Huntsman Knife',
        'class': WeaponClass.KNIFE,
        'ent_class': 'weapon_knife_tactical'
    },
    512: {
        'name': 'Falchion Knife',
        'class': WeaponClass.KNIFE,
        'ent_class': 'weapon_knife_falchion'
    },
    514: {
        'name': 'Bowie Knife',
        'class': WeaponClass.KNIFE,
        'ent_class': 'weapon_knife_survival_bowie'
    },
    515: {
        'name': 'Butterfly Knife',
        'class': WeaponClass.KNIFE,
        'ent_class': 'weapon_knife_butterfly'
    },
    516: {
        'name': 'Shadow Daggers',
        'class': WeaponClass.KNIFE,
        'ent_class': 'weapon_knife_push'
    }
}


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
        return weapon_ids.get(self.item_index, {}).get('name')

    @property
    def weapon_class(self):
        return weapon_ids.get(self.item_index, {}).get('class')

    @property
    def entity_class(self):
        return weapon_ids.get(self.item_index, {}).get('ent_class')

    @property
    def previous_owner(self):
        handle = self.get_prop('DT_WeaponCSBase', 'm_hPrevOwner')
        return self.parser.entities.get_by_handle(handle)

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
