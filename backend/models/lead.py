from database import db

class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(50))
    contact_person = db.Column(db.String(100))
    stage = db.Column(db.String(50), default="New Lead")
    ai_score = db.Column(db.Integer, default=0)

    def to_dict(self):
        """Utility method to easily convert the object to JSON for the API."""
        return {
            "id": self.id,
            "company": self.company,
            "industry": self.industry,
            "contact_person": self.contact_person,
            "stage": self.stage,
            "score": self.ai_score
        }