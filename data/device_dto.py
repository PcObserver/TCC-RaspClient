from typing import TypedDict
from data.user_dto import UserDTO
from models.device import Device


class DeviceDTO(TypedDict):
    id: str
    display_name: str
    parent_brand: str
    created_at: str
    updated_at: str
    user_id: UserDTO
    positive_reviews_count: int
    actions_count: int

    def parse():
        Device(
            id=DeviceDTO['id'],
            name=DeviceDTO['display_name'],
            parent_brand=DeviceDTO['parent_brand'],
        )

