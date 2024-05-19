from dataclasses import dataclass
from data.user_dto import UserDTO
from models.device import Device
from uuid import UUID
from datetime import datetime

@dataclass
class DeviceDTO:
    id: UUID
    display_name: str
    parent_brand: UUID
    created_at: datetime
    updated_at: datetime
    user: UserDTO
    positive_reviews_count: int
    actions_count: int

    def __post_init__(self):
        self.id = UUID(self.id)
        self.parent_brand = UUID(self.parent_brand)
        self.created_at = datetime.fromisoformat(self.created_at)
        self.updated_at = datetime.fromisoformat(self.updated_at)
        self.user = UserDTO(**self.user)

    def parse(self):
        return Device(
            id=self.id,
            name=self.display_name,
            brand_id=self.parent_brand
        )

