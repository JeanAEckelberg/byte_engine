from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.items.item import Item
from game.common.stations.station import Station
from typing import Self

# create station object that contains occupied_by
class Occupiable_Station(Station):
    def __init__(self, item: Item = None, occupied_by: bool = False):
        super().__init__(self, item)
        self.object_type = ObjectType.OCCUPIABLE_STATION
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
    
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.occupied_by = data['occupied_by']

        # framework match case for from json, can add more cases if they can occupy station
        match self.occupied_by["object_type"]:
            case ObjectType.AVATAR:
                self.occupied_by = Avatar().from_json(data['occupied_by'])
            case _:
                raise Exception(f'Could not parse occupied_by: {self.occupied_by}')           
            
        return self

        