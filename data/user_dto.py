from typing import TypedDict


class UserDTO(TypedDict):
    id: str
    email: str
    name: str
    date_joined: str

    