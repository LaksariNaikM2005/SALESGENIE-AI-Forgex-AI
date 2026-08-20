from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import os

app = Flask(__name__)
# Database & JWT Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../../sales.db')
app.config['JWT_SECRET_KEY'] = 'vtusalesgenie-secure-key-2026'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Database Models
class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(50))
    stage = db.Column(db.String(50), default="New Lead")
    ai_score = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

# Core CRUD & Data Routes
@app.route('/api/leads', methods=['GET', 'POST'])
def manage_leads():
    if request.method == 'POST':
        data = request.json
        new_lead = Lead(
            company=data['company'], 
            industry=data.get('industry', 'Unknown'),
            ai_score=data.get('score', 0)
        )
        db.session.add(new_lead)
        db.session.commit()
        return jsonify({"message": "Lead added successfully"}), 201
    
    leads = Lead.query.all()
    return jsonify([{"id": l.id, "company": l.company, "stage": l.stage, "score": l.ai_score} for l in leads])

if __name__ == '__main__':
    app.run(debug=True, port=5000)