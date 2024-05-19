from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from application import db
import uuid


class Brand(db.Model):
    __tablename__ = "brands"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(25), unique=True, nullable=False)
    prefix = db.Column(db.String(25), unique=True, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now())

    def to_select2_dict(self):
        return {
            "id": self.id,
            "text": self.name,
        }
    