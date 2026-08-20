try:
    from extensions import db
except ImportError:
    from backend.extensions import db
from datetime import datetime, timezone

class FollowUp(db.Model):
    __tablename__ = 'follow_ups'
    
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, nullable=False)
    due_at = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.String(50), default="Normal")
    status = db.Column(db.String(50), default="Pending")
    notes = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True)
