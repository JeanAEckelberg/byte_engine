from game.common.action import Action
from game.common.game_object import GameObject
from game.common.avatar import Avatar
from game.common.enums import *


class Player(GameObject):
    def __init__(self, code: object | None = None, team_name: str | None = None, action: ActionType | None = None,
                 avatar: Avatar | None = None):
        super().__init__()
        self.object_type: ObjectType = ObjectType.PLAYER
        self.functional: bool = True
        self.error: object | None = None
        self.team_name: str | None = team_name
        self.code: object = code
        # self.action: Action = action
        self.action: ActionType = action
        self.avatar: Avatar = avatar

    @property
    def action(self) -> ActionType | None:  # change to Action if you want to use the action object
        return self.__action

    @action.setter
    def action(self, action: ActionType | None):
        if action is not None or not isinstance(action, ActionType):
            # ^change to Action if you want to use the action object
            raise ValueError(f'{self.__class__.__name__}.action must be ActionType or None')
            # ^if it's not either throw an error
        self.__action = action

    @property
    def functional(self) -> bool:
        return self.__functional

    @functional.setter  # do this for all the setters
    def functional(self, functional: bool):  # this enforces the type intting
        if functional is None or not isinstance(functional, bool):  # if this statement is true throw an error
            raise ValueError(f'{self.__class__.__name__}.functional must be a boolean')
        self.__functional = functional

    @property
    def team_name(self) -> str:
        return self.__team_name

    @team_name.setter
    def team_name(self, team_name: str):
        if team_name is not None or not isinstance(team_name, str):
            raise ValueError(f'{self.__class__.__name__}.team_name must be a String')
        self.__team_name = team_name

    @property
    def avatar(self) -> Avatar:
        return self.__avatar

    @avatar.setter
    def avatar(self, avatar: Avatar):
        if avatar is None or not isinstance(avatar, Avatar):
            raise ValueError(f'{self.__class__.__name__}.avatar must be Avatar')
        self.__avatar = avatar

    @property
    def object_type(self) -> ObjectType:
        return self.object_type

    @object_type.setter
    def object_type(self, object_type: ObjectType):
        if object_type is None or not isinstance(object_type, GameObject):
            raise ValueError(f'{self.__class__.__name__}.object_type must be ObjectType')
        self.__object_type = object_type

    def to_json(self):
        data = super().to_json()

        data['functional'] = self.functional
        data['error'] = self.error
        data['team_name'] = self.team_name
        data['action'] = self.action.to_json() if self.action is not None else None
        data['avatar'] = self.avatar.to_json() if self.avatar is not None else None

        return data

    def from_json(self, data):
        super().from_json(data)
        
        self.functional = data['functional']
        self.error = data['error']
        self.team_name = data['team_name']
        self.action = Action().from_json(data['action']) if data['action'] is not None else None
        self.avatar = Avatar().from_json(data['avatar']) if data['avatar'] is not None else None

    def __str__(self):
        p = f"""ID: {self.id}
            Team name: {self.team_name}
            Action: {self.action}
            """
        return p
