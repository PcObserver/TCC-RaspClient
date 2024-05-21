from dataclasses import dataclass
from data.user_dto import UserDTO
from models.brand import Brand
from uuid import UUID
from datetime import datetime

@dataclass
class BrandDTO:
    id: UUID
    display_name: str
    description: str
    prefix: str
    created_at: datetime
    updated_at: datetime
    user: UserDTO
    devices_count: int
    positive_reviews_count: int

    def __post_init__(self):
        self.id = UUID(self.id)
        self.user = UserDTO(**self.user) if self.user else None
        self.created_at = datetime.fromisoformat(self.created_at)
        self.updated_at = datetime.fromisoformat(self.updated_at)
    
    def parse(self):
        return Brand(
            id=self.id,
            name=self.display_name,
            prefix=self.prefix,
        )
    