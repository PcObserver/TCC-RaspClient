from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from application import db
import uuid

class Device(db.Model):
    __tablename__ = "devices"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id = db.Column(UUID(as_uuid=True), db.ForeignKey("brands.id"), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now())
