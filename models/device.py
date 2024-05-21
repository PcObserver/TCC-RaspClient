from sqlalchemy import desc
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from application import db
import uuid

class Device(db.Model):
    __tablename__ = "devices"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    brand_id = db.Column(UUID(as_uuid=True), db.ForeignKey("brands.id"), nullable=False)
    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey("authors.id"), nullable=True)
    contribution_id = db.Column(UUID(as_uuid=True), nullable=True)

    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now())

    brand = db.relationship("Brand", backref="devices")
    user_devices = db.relationship("UserDevice", back_populates="device")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "brand_id": self.brand_id,
        }
    
    def to_select2_dict(self):
        return {
            "id": self.id,
            "text": self.name,
        }
