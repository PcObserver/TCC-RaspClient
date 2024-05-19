from dataclasses import dataclass
from data.user_dto import UserDTO
from models.action import Action, RequestMethod, ConnectionProtocol
from uuid import UUID
from datetime import datetime
import json
from uuid import UUID
@dataclass
class ActionDTO:
    id: UUID
    name: str
    parent_device: UUID 
    method: RequestMethod
    protocol: ConnectionProtocol
    path: str
    payload: json = None
    created_at: str = None
    updated_at: str = None
    user: UserDTO = None
    positive_reviews_count: int = 0

    def __post_init__(self):
        self.id = str(UUID(self.id))
        self.user = UserDTO(**self.user) if self.user else None
        self.parent_device = str(UUID(self.parent_device))
        self.created_at = datetime.fromisoformat(self.created_at)
        self.updated_at = datetime.fromisoformat(self.updated_at)
        self.method = RequestMethod(self.method)
        self.protocol = ConnectionProtocol(self.protocol)


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
