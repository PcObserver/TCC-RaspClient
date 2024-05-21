from dataclasses import dataclass
from data.user_dto import UserDTO
from models.action import Action, RequestMethod, ConnectionProtocol
from uuid import UUID
from datetime import datetime
import json


@dataclass
class ActionDTO:
    id: UUID
    name: str
    description: str
    parent_device: UUID 
    method: RequestMethod
    protocol: ConnectionProtocol
    path: str
    payload: json = None
    created_at: str = None
    updated_at: str = None
    user: UserDTO = None
    positive_reviews_count: int = 0
    contribuition_type: str = None

    def __post_init__(self):
        self.id = UUID(self.id)
        self.user = UserDTO(**self.user) if self.user else None
        self.parent_device = UUID(self.parent_device)
        self.created_at = datetime.fromisoformat(self.created_at)
        self.updated_at = datetime.fromisoformat(self.updated_at)
        self.method = RequestMethod(self.method).value
        self.protocol = ConnectionProtocol(self.protocol).value

    def parse(self):
        return Action(
            name=self.name,
            description=self.description,
            path="PATH",
            device_id=self.parent_device,
            request_method=self.method,
            connection_protocol=self.protocol,
            payload=self.payload,
            author_id=self.user.id,
            contribuition_id=self.id
        )
