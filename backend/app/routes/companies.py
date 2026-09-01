from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import Company

companies_bp = Blueprint("companies", __name__, url_prefix="/api/companies")

@companies_bp.get("")
@jwt_required()
def get_companies():
    query = Company.query
    search = request.args.get("search")
    if search:
        query = query.filter(Company.name.ilike(f"%{search}%") | Company.industry.ilike(f"%{search}%"))
    
    companies = query.order_by(Company.name.asc()).all()
    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "industry": c.industry,
            "size": c.size,
            "annual_revenue": c.annual_revenue,
            "location": c.location,
            "employee_count": c.employee_count,
            "website": c.website,
            "technology_stack": c.technology_stack,
            "products_services": c.products_services,
            "funding": c.funding,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        } for c in companies
    ]), 200

@companies_bp.post("")
@jwt_required()
def create_company():
    data = request.get_json() or {}
    if not data.get("name"):
        return jsonify({"message": "Company name is required"}), 400

    company = Company(
        name=data.get("name"),
        industry=data.get("industry"),
        size=data.get("size"),
        annual_revenue=data.get("annual_revenue"),
        location=data.get("location"),
        employee_count=data.get("employee_count"),
        website=data.get("website"),
        technology_stack=data.get("technology_stack"),
        products_services=data.get("products_services"),
        funding=data.get("funding"),
    )
    db.session.add(company)
    db.session.commit()

    return jsonify({
        "id": company.id,
        "name": company.name,
        "message": "Company created successfully"
    }), 201

@companies_bp.get("/<int:company_id>")
@jwt_required()
def get_company(company_id):
    company = db.session.get(Company, company_id)
    if not company:
        return jsonify({"message": "Company not found"}), 404

    return jsonify({
        "id": company.id,
        "name": company.name,
        "industry": company.industry,
        "size": company.size,
        "annual_revenue": company.annual_revenue,
        "location": company.location,
        "employee_count": company.employee_count,
        "website": company.website,
        "technology_stack": company.technology_stack,
        "products_services": company.products_services,
        "funding": company.funding,
        "contacts": [
            {
                "id": ct.id,
                "name": ct.name,
                "designation": ct.designation,
                "email": ct.email,
                "phone": ct.phone,
                "is_decision_maker": ct.is_decision_maker,
            } for ct in company.contacts
        ]
    }), 200
