from dataclasses import dataclass
from data.user_dto import UserDTO
from models.action import Action
from uuid import UUID
from datetime import datetime
@dataclass
class ActionDTO:
    id: str
    name: str
    parent_device: str
    method: str
    protocol: str
    path: str
    payload: str
    created_at: str
    updated_at: str
    user: UserDTO
    positive_reviews_count: int

    def __post_init__(self):
        self.id = str(UUID(self.id))
        self.user = UserDTO(**self.user)
        self.created_at = datetime.fromisoformat(self.created_at)
        self.updated_at = datetime.fromisoformat(self.updated_at)

    def parse(self):
        return Action(
            id=self.id,
            name=self.display_name,
            device_id=self.parent_device,
            request_method=self.method,
            connection_protocol=self.protocol,
            path=self.path,
            payload=self.payload,
        )
