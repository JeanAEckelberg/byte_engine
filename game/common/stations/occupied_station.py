from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.items.item import Item
from game.common.stations.station import Station

# create station object that contains occupied_by
class Occupied_Station(Station):
    def __init__(self, item: Item = None, occupied_by: bool = False):
        super().__init__(self, item)
        self.object_type = ObjectType.occupied_station
        self.occupied_by = occupied_by

    # occupied_by getter and setter methods
    @property
    def occupied_by(self) -> bool:
        return self.occupied_by
    
    @occupied_by.setter
    def occupied_by(self, occupied_by: bool):
        self.occupied_by = occupied_by

    # take action method
    def take_action(self, avatar: Avatar = None):
        return
    
    # json methods
    def to_json(self) -> dict:
        dict_data = super().to_json()
        dict_data['occupied_by'] = self.occupied_by
        return dict_data
    
    def from_json(self, data: dict) -> 'Occupied_Station':
        super().from_json(data)
        self.occupied_by = data['occupied_by']
        return self

        