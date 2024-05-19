from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from application import db
from enum import Enum
import uuid


class ConnectionProtocol(Enum):
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    MQTT = "MQTT"


class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class Action(db.Model):
    __tablename__ = "actions"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = db.Column(db.String)
    path = db.Column(db.String)
    device_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("devices.id"), nullable=False
    )
    name = db.Column(db.String)
    payload = db.Column(db.JSON)
    request_method = db.Column(db.Enum(RequestMethod), default=RequestMethod.POST)
    connection_protocol = db.Column(db.Enum(ConnectionProtocol), default=ConnectionProtocol.HTTP)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now())
    device = db.relationship("Device", backref="actions")


    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "path": self.path,
            "device_id": self.device_id,
            "payload": self.payload,
            "request_method": self.request_method,
            "connection_protocol": self.connection_protocol,
        }

