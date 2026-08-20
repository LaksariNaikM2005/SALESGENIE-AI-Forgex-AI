try:
    from extensions import db
except ImportError:
    from backend.extensions import db
from datetime import datetime, timezone

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(100), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
