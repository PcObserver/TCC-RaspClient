from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from application import db
import uuid


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String)
    email = db.Column(db.String)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now())

    brands = db.relationship("Brand", back_populates="author")
    devices = db.relationship("Device", back_populates="author")
    actions = db.relationship("Action", back_populates="author")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }
