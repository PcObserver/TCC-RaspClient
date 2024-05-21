from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from models.author import Author
@dataclass
class UserDTO:
    id: UUID
    email: str
    name: str
    date_joined: datetime

    def __post_init__(self):
        self.id = UUID(self.id)
        self.date_joined = datetime.fromisoformat(self.date_joined)
    
    def parse(self):
        return Author(
            id=self.id,
            email=self.email,
            name=self.name
        )

    