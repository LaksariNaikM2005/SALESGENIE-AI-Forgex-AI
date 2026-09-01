from datetime import datetime, timezone
from ..extensions import db

class CRMConnection(db.Model):
    __tablename__ = "crm_connections"

    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(50), nullable=False) # salesforce, hubspot
    account_name = db.Column(db.String(120), nullable=True)
    access_token = db.Column(db.Text, nullable=True)
    refresh_token = db.Column(db.Text, nullable=True)
    instance_url = db.Column(db.String(255), nullable=True)
    sync_status = db.Column(db.String(50), nullable=False, default="Disconnected") # Connected, Syncing, Disconnected, Error
    last_sync_at = db.Column(db.DateTime(timezone=True), nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
