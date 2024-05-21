from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from application import db
import uuid


class Brand(db.Model):
    __tablename__ = "brands"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(25), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=True)
    prefix = db.Column(db.String(25), unique=True, nullable=False)
    contribution_id = db.Column(UUID(as_uuid=True), nullable=True)
    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey("authors.id"), nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now())
    author = db.relationship("Author", back_populates="brands")

    def to_select2_dict(self):
        return {
            "id": self.id,
            "text": self.name,
        }
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "prefix": self.prefix,
            "contribution_id": self.contribution_id,
            "author_id": self.author_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    