from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import Contact

contacts_bp = Blueprint("contacts", __name__, url_prefix="/api/contacts")

@contacts_bp.get("")
@jwt_required()
def get_contacts():
    company_id = request.args.get("company_id")
    query = Contact.query
    if company_id:
        query = query.filter_by(company_id=company_id)
    
    contacts = query.all()
    return jsonify([
        {
            "id": c.id,
            "company_id": c.company_id,
            "name": c.name,
            "designation": c.designation,
            "email": c.email,
            "phone": c.phone,
            "is_decision_maker": c.is_decision_maker,
            "decision_role": c.decision_role,
        } for c in contacts
    ]), 200

@contacts_bp.post("")
@jwt_required()
def create_contact():
    data = request.get_json() or {}
    if not data.get("name"):
        return jsonify({"message": "Contact name is required"}), 400

    contact = Contact(
        company_id=data.get("company_id"),
        name=data.get("name"),
        designation=data.get("designation"),
        email=data.get("email"),
        phone=data.get("phone"),
        is_decision_maker=data.get("is_decision_maker", False),
        decision_role=data.get("decision_role"),
    )
    db.session.add(contact)
    db.session.commit()

    return jsonify({
        "id": contact.id,
        "name": contact.name,
        "message": "Contact created successfully"
    }), 201
