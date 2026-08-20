from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)
engine = create_engine("sqlite:///sales.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    stage = Column(String, default="New Lead")
    ai_score = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

@app.route('/api/leads', methods=['GET', 'POST'])
def manage_leads():
    session = SessionLocal()
    if request.method == 'POST':
        data = request.json
        new_lead = Lead(company=data['company'], stage=data.get('stage', 'New Lead'), ai_score=data.get('score', 0))
        session.add(new_lead)
        session.commit()
        return jsonify({"message": "Lead added"}), 201
    
    leads = session.query(Lead).all()
    return jsonify([{"id": l.id, "company": l.company, "stage": l.stage, "score": l.ai_score} for l in leads])

if __name__ == '__main__':
    app.run(debug=True, port=5000)