import unittest

from game.common.enums import ObjectType
from game.common.avatar import Avatar
from game.common.items.item import Item
from game.common.stations.station import Station
from game.common.stations.occupiable_station import Occupiable_Station
from game.common.map.tile import Tile
from game.common.map.wall import Wall
from game.utils.vector import Vector

# class to test initialization of objects
class TestInitialization(unittest.TestCase):
    def setUp(self) -> None:
        self.item: Item = Item(10, 100)
        self.avatar: Avatar = Avatar(None, None)
        self.station: Station = Station(None)
        self.occupiable_station: Occupiable_Station = Occupiable_Station(None, None)
        self.tile: Tile = Tile(None)
        self.wall: Wall = Wall()
    
    # tests that all objects have the correct ObjectType
    def testObjectInit(self):
        self.assertEqual(self.item.object_type, ObjectType.ITEM)
        self.assertEqual(self.avatar.object_type, ObjectType.AVATAR)
        self.assertEqual(self.station.object_type, ObjectType.STATION)
        self.assertEqual(self.occupiable_station.object_type, ObjectType.OCCUPIABLE_STATION)
        self.assertEqual(self.tile.object_type, ObjectType.TILE)
        self.assertEqual(self.wall.object_type, ObjectType.WALL)

