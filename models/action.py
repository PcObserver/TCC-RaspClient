from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from application import db


class Action(db.Model):
    __tablename__ = "actions"

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    device_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("devices.id"), nullable=False
    )
    name = db.Column(db.String)
    payload = db.Column(db.JSON)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now())
