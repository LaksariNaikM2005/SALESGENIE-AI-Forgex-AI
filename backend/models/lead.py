try:
    from extensions import db
except ImportError:
    from backend.extensions import db

class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), default="")
    industry = db.Column(db.String(50), default="")
    revenue = db.Column(db.Float, default=0.0)
    stage = db.Column(db.String(50), default="New Lead")
    score = db.Column(db.Integer, default=0)
    category = db.Column(db.String(20), default="Cold")
    notes = db.Column(db.Text, default="")
    
    # Compatibility properties for the new contact_person and ai_score fields
    @property
    def contact_person(self):
        return self.contact
        
    @contact_person.setter
    def contact_person(self, value):
        self.contact = value
        
    @property
    def ai_score(self):
        return self.score
        
    @ai_score.setter
    def ai_score(self, value):
        self.score = value

    def to_dict(self):
        """Utility method to easily convert the object to JSON for the API."""
        return {
            "id": self.id,
            "company": self.company,
            "contact": self.contact,
            "contact_person": self.contact_person,
            "designation": self.designation,
            "industry": self.industry,
            "revenue": self.revenue,
            "stage": self.stage,
            "score": self.score,
            "ai_score": self.ai_score,
            "category": self.category,
            "notes": self.notes
        }