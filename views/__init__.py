from .application import application_blueprint
from .device import device_blueprint
from .brand import brand_blueprint
from .user_device import user_device_blueprint
from .action import action_blueprint
from .auth import auth_blueprint

__all__ = [
    "application_blueprint",
    "device_blueprint",
    "brand_blueprint",
    "user_device_blueprint",
    "action_blueprint",
    "auth_blueprint",
]
