from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from application import db
import uuid


class UserDevice(db.Model):
    __tablename__ = "user_devices"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nickname = db.Column(db.String)
    serial = db.Column(db.String)
    hostname = db.Column(db.String)
    port = db.Column(db.Integer)
    address = db.Column(db.String)
    device_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("devices.id"), nullable=False
    )

    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now())

    device = db.relationship("Device", back_populates="user_devices")
