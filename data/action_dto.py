from typing import TypedDict
from data.user_dto import UserDTO
from models.action import Action


class ActionDTO(TypedDict):
    id: str
    display_name: str
    parent_device: str
    method: str
    protocol: str
    path: str
    payload: str
    created_at: str
    updated_at: str
    user_id: UserDTO
    positive_reviews_count: int
    actions_count: int

    def parse():
        Action(
              id=ActionDTO['id'],
              name=ActionDTO['display_name'],
              device_id=ActionDTO['parent_device'],
              request_method=ActionDTO['method'],
              connection_protocol=ActionDTO['protocol'],
              path=ActionDTO['path'],
              payload=ActionDTO['payload'],
        )
