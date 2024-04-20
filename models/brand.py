from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from application import db


class Brand(db.Model):
    __tablename__ = "brands"

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    display_name = db.Column(db.String)
    perma_name = db.Column(db.String)
    prefix = db.Column(db.String)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now())
