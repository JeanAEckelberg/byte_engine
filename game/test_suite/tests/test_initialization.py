import unittest

from game.common.enums import ObjectType
from game.common.avatar import Avatar
from game.common.items.item import Item
from game.common.stations.station import Station
from game.common.map.tile import Tile, Occupiable_Station
from game.common.map.wall import Wall

class TestInitialization(unittest.TestCase):
    def setUp(self) -> None:
        self.item = Item(10, 100)
        self.avatar = Avatar(None, None)
        self.station = Station(None)
        self.occupiable_station = Occupiable_Station(None, None)
        self.tile = Tile(None)
        self.wall = Wall()
    

    def testObjectInit(self):
        self.assertEqual(self.item.object_type, ObjectType.ITEM)
        self.assertEqual(self.avatar.object_type, ObjectType.AVATAR)
        self.assertEqual(self.station.object_type, ObjectType.STATION)
        self.assertEqual(self.occupiable_station.object_type, ObjectType.OCCUPIABLE_STATION)
        self.assertEqual(self.tile.object_type, ObjectType.TILE)
        self.assertEqual(self.wall.object_type, ObjectType.WALL)

    def testAvatarSetItem(self):
        self.avatar.held_item = self.item
        self.assertEqual(self.avatar.held_item, self.item)

    def testAvatarSetItemFail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.held_item = 3
        self.assertEqual(str(e.exception), 'Avatar.held_item must be an Item or None.')

    def testAvatarSetScore(self):
        self.avatar.score = 10
        self.assertEqual(self.avatar.score, 10)

    def testAvatarSetScoreFail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.score = 'wow'
        self.assertEqual(str(e.exception), 'Avatar.score must be an int.')


    def testAvatarSetPosition(self):
        self.avatar.position = (10, 10)
        self.assertEqual(self.avatar.position, (10, 10))

    def testAvatarSetPositionFail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.position = 10
        self.assertEqual(str(e.exception), 'Avatar.position must be a tuple of two ints or None.')

if __name__ == '__main__':
    unittest.main()