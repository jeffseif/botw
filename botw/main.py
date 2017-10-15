from collections import defaultdict
import json
import xml.etree.ElementTree as ET


DAT = './dat/'
MISSING = '<MISSING NAME>'


class InvalidActorException(Exception):
    pass


class Actor:

    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def __str__(self):
        return '\n'.join(
            '{:s}\t{:s}'.format(attr, repr(getattr(self, attr)))
            for attr in sorted(self.__dict__)
        )

    @classmethod
    def from_xml(cls, the_xml):
        try:
            return cls._from_xml(the_xml)
        except AssertionError:
            return
        except AttributeError:
            return
        except TypeError:
            return


class Armor(Actor):

    ING_KEYS = tuple(
        ('normal0ItemName{:02d}'.format(n), 'normal0ItemNum{:02d}'.format(n))
        for n in range(100)
    )

    JEWELRY_SERIES = (
        'Amber',
        'Dia',
        'Opal',
        'Ruby',
        'Sapphire',
        'SheikMask',
        'Topaz',
    )

    def __bool__(self):
        return (
            bool(self.series_name.strip())
            and not 'Amiibo' in self.series_name
            and self.series_name not in self.JEWELRY_SERIES
        )

    @classmethod
    def _from_xml(cls, the_xml):
        return cls(
            #
            defense = int(the_xml.get('armorDefenceAddLevel')),
            stars = int(the_xml.get('armorStarNum')),
            #
            id = the_xml.find('name').text,
            series_name = the_xml.find('seriesArmorSeriesType').text,
            #
            ingredients = {
                the_xml.find(name_key).text: int(the_xml.get(number_key))
                for name_key, number_key in cls.ING_KEYS
                if the_xml.find(name_key) is not None
            },
        )


class Weapon(Actor):

    MAX_ATTACK = 116

    def __bool__(self):
        return (
            hasattr(self, 'id')
            and self.attack > 0
        )

    @property
    def max_attack(self):
        return min(self.MAX_ATTACK, (self.attack + self.buff))

    @classmethod
    def _from_xml(cls, the_xml):
        assert 'weapon' in the_xml.find('xlink').text.lower()
        return cls(
            attack = int(the_xml.get('attackPower')),
            buff = int(the_xml.get('weaponCommonPoweredSharpAddAtkMax')),
            durability = int(the_xml.get('generalLife')),
            id = the_xml.find('name').text,
        )


def get_names():
    with open('{:s}botw_names.json'.format(DAT), 'rt') as f:
        return json.load(f)

    armor = {}
    for id, name in dat.items():
        if 'Armor' in id:
            if name not in armor:
                armor[name] = set((id, ))
            else:
                armor[name].add(id)
    return armor


def get_actors(cls):
    with open('{:s}ActorInfo.product.xml'.format(DAT), 'rt') as f:
        root = ET.parse(f).getroot()
    
    actors = root.find('Actors')
    return [
        actor
        for actor in map(cls.from_xml, actors)
        if actor is not None
        if actor
    ]


def summarize(title, name_counts):
    counts = defaultdict(int)
    for name, count in name_counts:
        counts[name] += count

    if counts:
        yield json.dumps({
            'title': title,
            'data': dict(counts)
        })



def report_armors(armors):

    armor_ids = {
        armor.id
        for armor in armors
    }

    series_names = {
        armor.series_name
        for armor in armors
    }

    for series_name in sorted(series_names):
        yield from summarize(
            'Full {:s} armor'.format(series_name),
            (
                (NAMES[ingredient], count)
                for armor in armors
                if armor.series_name == series_name
                if armor.ingredients
                for ingredient, count in armor.ingredients.items()
                if ingredient not in armor_ids
            ),
        )
    
    for stars in range(6):
        yield from summarize(
            'All armors at {:d} stars'.format(stars - 1),
            (
                (NAMES[ingredient], count)
                for armor in armors
                if armor.stars == stars
                for ingredient, count in armor.ingredients.items()
                if ingredient not in armor_ids
            ),
        )

    yield from summarize(
        'All armors',
        (
            (NAMES[ingredient], count)
            for armor in armors
            for ingredient, count in armor.ingredients.items()
            if ingredient not in armor_ids
        ),
    )


def report_weapons(weapons):
    yield from summarize(
        'Weapon Base Attacks',
        (
            (NAMES.get(weapon.id, MISSING), weapon.attack)
            for weapon in weapons
        ),
    )
    return

    yield from summarize(
        'Weapon Max Attacks',
        (
            (NAMES.get(weapon.id, MISSING), weapon.max_attack)
            for weapon in weapons
        ),
    )

    yield from summarize(
        'Weapon Durabilities',
        (
            (NAMES.get(weapon.id, MISSING), weapon.durability)
            for weapon in weapons
        ),
    )


if __name__ == '__main__':
    if 'armors' in __file__:
        cls = Armor
        reporter = report_armors
    elif 'weapons' in __file__:
        cls = Weapon
        reporter = report_weapons

    NAMES = get_names()
    for report in reporter(get_actors(cls)):
        print(report)
