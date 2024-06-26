from dataclasses import dataclass
from data.user_dto import UserDTO
from models.device import Device
from uuid import UUID
from datetime import datetime


@dataclass
class DeviceDTO:
    id: UUID
    display_name: str
    description: str
    parent_brand: UUID
    prefix: str = None
    contribution_type: str = None
    created_at: datetime = None
    updated_at: datetime = None
    user: UserDTO = None
    positive_reviews_count: int = 0
    actions_count: int = 0

    def __post_init__(self):
        self.id = UUID(self.id)
        self.parent_brand = UUID(self.parent_brand)
        self.created_at = datetime.fromisoformat(self.created_at)
        self.updated_at = datetime.fromisoformat(self.updated_at)
        self.user = UserDTO(**self.user) if self.user else None

    def parse(self):
        return Device(
            name=self.display_name,
            description=self.description,
            prefix=self.prefix,
            brand_id=self.parent_brand,
            contribution_id=self.id,
            author_id=self.user.id,
        )
