from collections import defaultdict
import json
import xml.etree.ElementTree as ET


DAT = './dat/'


class InvalidActorException(Exception):
    pass


class Actor:

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
        'Topaz',
    )

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
            return cls(
                #
                defense = int(the_xml.get('armorDefenceAddLevel')),
                stars = int(the_xml.get('armorStarNum')),
                #
                base_id = the_xml.find('mainModel').text,
                id = the_xml.find('name').text,
                series_id = the_xml.find('bfres').text,
                series_name = the_xml.find('seriesArmorSeriesType').text,
                #
                ingredients = {
                    the_xml.find(name_key).text: int(the_xml.get(number_key))
                    for name_key, number_key in cls.ING_KEYS
                    if the_xml.find(name_key) is not None
                },
            )
        except AttributeError:
            return
        except TypeError:
            return

    def is_good(self):
        return (
            self.series_name.strip()
            and not 'Amiibo' in self.series_name
            and self.series_name not in self.JEWELRY_SERIES
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


def get_armors():
    with open('{:s}ActorInfo.product.xml'.format(DAT), 'rt') as f:
        root = ET.parse(f).getroot()
    
    actors = root.find('Actors')
    return [
        actor
        for actor in map(Actor.from_xml, actors)
        if actor is not None
        if actor.is_good()
    ]


def jsonify(format, key, ingredients):
    counts = defaultdict(int)
    for ingredient, count in ingredients:
        counts[ingredient] += count

    if not counts:
        return

    yield json.dumps({
        'title': format.format(key),
        'data': dict(counts)
    })


def slices(armors, names):

    armor_ids = {
        armor.id
        for armor in armors
    }

    series_names = {
        armor.series_name
        for armor in armors
    }

    for series_name in sorted(series_names):
        yield from jsonify(
            'Full {:s} armor',
            series_name,
            (
                (names[ingredient], count)
                for armor in armors
                if armor.series_name == series_name
                if armor.ingredients
                for ingredient, count in armor.ingredients.items()
                if ingredient not in armor_ids
            ),
        )
    
    for stars in range(6):
        yield from jsonify(
            'All armors at {:d} stars',
            stars - 1,
            (
                (names[ingredient], count)
                for armor in armors
                if armor.stars == stars
                for ingredient, count in armor.ingredients.items()
                if ingredient not in armor_ids
            ),
        )

    yield from jsonify(
        'All armors',
        '',
        (
            (names[ingredient], count)
            for armor in armors
            for ingredient, count in armor.ingredients.items()
            if ingredient not in armor_ids
        ),
    )


def main():
    names = get_names()
    armors = get_armors()
    for slice in slices(armors, names):
        print(slice)


if __name__ == '__main__':
    main()
