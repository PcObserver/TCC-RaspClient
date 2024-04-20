from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from application import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    device_id = db.Column(UUID(as_uuid=True), db.ForeignKey("devices.id"))
    name = db.Column(db.String)
    email = db.Column(db.String)
    encrypted_password = db.Column(db.String)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now())
