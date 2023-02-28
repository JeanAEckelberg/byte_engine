from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.enums import ObjectType
from game.common.items.item import Item

# create Station object from GameObject that allows item to be contained in it
class Station(GameObject):
    def __init__(self, item: Item = None):
        super().__init__()
        self.object_type = ObjectType.station
        self.item: Item = item

    # item getter and setter methods
    @property
    def item(self) -> Item:
        return self.__item

    @item.setter
    def item(self, item: Item):
        self.__item = item if isinstance(item, Item) else None

    # take action method
    def take_action(self, avatar: Avatar = None):
        return

    # json methods
    def to_json(self) -> dict:
        dict_data = super().to_json()
        dict_data['item'] = self.item.to_json() if self.item else None

        return dict_data

    def from_json(self, data: dict) -> 'Station':
        super().from_json(data)
        if not data['item']:
            self.item = None

        return self
    