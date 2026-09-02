"""
FORGE_X AI - Complete Database Seeding & Reset Script
Populates demo users, imports all leads from the real-world dataset,
generates AI recommendations, and verifies database state.
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app
from backend.app.extensions import db
from backend.app.models import User, Lead, AIRecommendation

import pandas as pd
from pathlib import Path
from werkzeug.security import generate_password_hash

def seed_demo_users(app):
    """Creates demo accounts for all roles."""
    print("\n=== Seeding Demo Users ===")
    demo_users = [
        {"name": "Admin User",      "email": "admin@forgex.ai",    "password": "Admin@123",   "role": "admin"},
        {"name": "Sarah Mitchell",  "email": "manager@forgex.ai",  "password": "Manager@123", "role": "sales_manager"},
        {"name": "James Carter",    "email": "sales@forgex.ai",    "password": "Sales@123",   "role": "sales_rep"},
        {"name": "Priya Sharma",    "email": "priya@forgex.ai",    "password": "Priya@123",   "role": "sales_rep"},
        {"name": "Marcus Vance",    "email": "marcus@forgex.ai",   "password": "Marcus@123",  "role": "sales_rep"},
    ]

    with app.app_context():
        created = 0
        for ud in demo_users:
            existing = User.query.filter_by(email=ud["email"]).first()
            if not existing:
                user = User(
                    name=ud["name"],
                    email=ud["email"],
                    password_hash=generate_password_hash(ud["password"]),
                    role=ud["role"],
                    is_active=True,
                )
                db.session.add(user)
                created += 1
                print(f"  [+] Created: {ud['name']} ({ud['role']}) -> {ud['email']} / {ud['password']}")
            else:
                print(f"  [=] Exists: {ud['email']}")
        db.session.commit()
        print(f"  Demo users ready: {created} new created")


def seed_leads_from_csv(app, limit=None):
    """Imports real-world sales pipeline CSV into database with ML scoring."""
    from backend.app.services.lead_service import build_ml_input, safe_float, safe_int
    from ai_ml_engine.inference.predict import predict_lead

    print("\n=== Seeding Leads from Real-World Dataset ===")

    project_root = Path(__file__).resolve().parent
    raw_path = project_root / "ai_ml_engine" / "data" / "raw" / "sales_pipeline.csv"

    if not raw_path.exists():
        print(f"  ERROR: CSV not found at {raw_path}")
        return

    df = pd.read_csv(raw_path)
    if limit:
        df = df.head(limit)

    print(f"  Loading {len(df)} records from {raw_path.name}...")

    TECH_STACK_MAP = {
        "semi": "EUV Lithography, MES, Cleanroom SCADA, APC",
        "auto": "Automotive Stamping, ROS2, Vision Inspection, MES",
        "tool": "Fanuc CNC, High-Speed Spindles, CAD/CAM",
        "cnc":  "Fanuc CNC, High-Speed Spindles, CAD/CAM",
        "heavy": "Siemens S7 PLC, Heavy Hydraulics, SCADA",
        "elec": "PCB Assembly Line, AOI Systems, SMT Equipment",
        "robot": "KUKA Robots, ROS2, Force/Torque Sensors",
        "food": "HACCP Systems, Conveyor Automation, ERP",
        "pharm": "FDA-Compliant MES, Clean Room HVAC, Serialization",
    }

    def get_tech_stack(sector):
        s = str(sector).lower()
        for key, stack in TECH_STACK_MAP.items():
            if key in s:
                return stack
        return "ROS2, Siemens S7 PLC, Fanuc CNC, IoT Edge"

    def map_stage(deal_stage):
        s = str(deal_stage).strip().lower()
        if s == "won":     return "Won"
        if s == "lost":    return "Lost"
        if s == "proposal": return "Proposal"
        if s == "negotiation": return "Negotiation"
        if s == "qualified": return "Qualified"
        return "New Lead"

    with app.app_context():
        existing_count = Lead.query.count()
        if existing_count > 0:
            print(f"  Leads already exist ({existing_count}). Skipping import.")
            return

        batch_size = 100
        created = 0
        errors = 0

        for idx, row in df.iterrows():
            try:
                company   = str(row.get("account", f"Company_{idx}")).strip()
                agent     = str(row.get("sales_agent", "Marcus Vance")).strip()
                sector    = str(row.get("sector", "industrial_automation")).strip()
                product   = str(row.get("product", "Industrial Robot")).strip()
                deal_stage= str(row.get("deal_stage", "Qualified")).strip()
                revenue   = safe_float(row.get("revenue"), default=85.0)
                employees = safe_int(row.get("employees"), default=1450)
                deal_val  = safe_float(row.get("deal_value"), default=125000.0)
                sales_price = safe_float(row.get("sales_price"), default=deal_val)

                sector_clean = sector.replace("_", " ").title()
                email = f"contact.{idx}@{company.lower().replace(' ', '').replace('.', '')}.com"

                lead_payload = {
                    "account": company,
                    "company": company,
                    "sector": sector,
                    "product": product,
                    "sales_agent": agent,
                    "manager": str(row.get("manager", "Alex Vance")).strip(),
                    "regional_office": str(row.get("regional_office", "Midwest")).strip(),
                    "revenue": revenue,
                    "employees": employees,
                    "value": deal_val,
                    "sales_price": sales_price,
                    "year_established": safe_int(row.get("year_established"), default=1998),
                    "office_location": str(row.get("office_location", "United States")).strip(),
                    "series": str(row.get("series", "Industrial Automation")).strip(),
                }

                ml_input = build_ml_input(lead_payload)
                prediction = predict_lead(ml_input)

                lead = Lead(
                    company=company,
                    contact_name=f"Contact at {company}",
                    email=email,
                    value=deal_val,
                    sector=sector_clean,
                    product=product,
                    tech_stack=get_tech_stack(sector),
                    revenue=revenue,
                    employees=employees,
                    sales_agent=agent,
                    stage=map_stage(deal_stage),
                    status="Open" if map_stage(deal_stage) not in ["Won", "Lost"] else "Closed",
                    lead_score=prediction["lead_score"],
                    purchase_probability=prediction["purchase_probability"],
                )
                db.session.add(lead)
                created += 1

                if created % batch_size == 0:
                    db.session.commit()
                    print(f"  ... committed {created} leads so far")

            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"  [ERR] Row {idx}: {e}")

        db.session.commit()
        print(f"  [OK] Imported {created} leads ({errors} errors)")


def seed_recommendations(app):
    """Generate AI recommendations for all leads without one."""
    from backend.app.services.ai_service import create_recommendation

    print("\n=== Generating AI Recommendations ===")
    with app.app_context():
        leads_without_recs = (
            db.session.query(Lead)
            .outerjoin(AIRecommendation, Lead.id == AIRecommendation.lead_id)
            .filter(AIRecommendation.id == None)
            .all()
        )
        print(f"  Found {len(leads_without_recs)} leads needing recommendations")

        created = 0
        errors = 0
        for lead in leads_without_recs:
            try:
                create_recommendation(lead.id)
                created += 1
                if created % 50 == 0:
                    print(f"  ... generated {created} recommendations so far")
            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"  [ERR] Lead {lead.id}: {e}")

        print(f"  [OK] Generated {created} AI recommendations ({errors} errors)")


def verify_state(app):
    """Prints final database state."""
    print("\n=== Final Database State ===")
    with app.app_context():
        users = User.query.count()
        leads = Lead.query.count()
        recs  = AIRecommendation.query.count()
        print(f"  Users:           {users}")
        print(f"  Leads:           {leads}")
        print(f"  Recommendations: {recs}")

        # Print demo credentials
        print("\n=== Demo Login Credentials ===")
        demos = [
            ("Admin",   "admin@forgex.ai",   "Admin@123"),
            ("Manager", "manager@forgex.ai",  "Manager@123"),
            ("Sales",   "sales@forgex.ai",    "Sales@123"),
        ]
        for role, email, pw in demos:
            print(f"  {role:10s}: {email:25s} / {pw}")


if __name__ == "__main__":
    print("FORGE_X AI - Database Seeding Script")
    print("=" * 50)

    app = create_app()

    with app.app_context():
        db.create_all()
        print("[OK] Database tables ensured")

    seed_demo_users(app)
    seed_leads_from_csv(app)  # Full 5000 records
    seed_recommendations(app)
    verify_state(app)

    print("\n[DONE] Database seeding complete!")
