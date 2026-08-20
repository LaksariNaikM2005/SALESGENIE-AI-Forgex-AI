try:
    from extensions import db
except ImportError:
    from backend.extensions import db
from datetime import datetime, timezone

class Meeting(db.Model):
    __tablename__ = 'meetings'
    
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), default="")
    scheduled_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default="Scheduled")
    notes = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
