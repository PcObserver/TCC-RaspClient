from sqlalchemy.sql import func
import uuid

from application import db


class Brand(db.Model):
    __tablename__ = "brands"

    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    display_name = db.Column(db.String(255), nullable=False)
    perma_name = db.Column(db.String(255), nullable=False)
    prefix = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = db.Column(
        db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
