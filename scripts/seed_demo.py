from datetime import datetime, timezone
import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from werkzeug.security import generate_password_hash

from backend.app import create_app
from backend.app.extensions import db
from backend.app.models import (
    AIRecommendation,
    CRMConnection,
    Company,
    Contact,
    FollowUpHistory,
    Lead,
    LeadActivity,
    User,
)
from backend.app.services.ai_service import generate_all_recommendations
from backend.app.services.lead_service import build_ml_input
from ai_ml_engine.inference.predict import predict_lead

RAW_PIPELINE_PATH = Path(__file__).resolve().parent.parent / "ai_ml_engine" / "data" / "raw" / "sales_pipeline.csv"


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()

        # 1. Seed Demo Users across various enterprise roles (Requirement 3)
        users_to_seed = [
            ("System Administrator", "admin@salesgenie.ai", "AdminPass123!", "admin"),
            ("Alex Vance (Sales Director)", "manager@salesgenie.ai", "ManagerPass123!", "sales_manager"),
            ("Jordan Blake (Account Executive)", "rep@salesgenie.ai", "RepPass123!", "sales_rep"),
            ("Vikram Mehta (VP of Operations)", "vp.operations@salesgenie.ai", "VpPass123!", "sales_manager"),
            ("Dr. Aris Thorne (Chief Fab Architect)", "eng.lead@salesgenie.ai", "EngPass123!", "sales_rep"),
            ("Laksari Naik", "laksarin.manager@sales.com", "Password123!", "sales_manager"),
            ("Laksari Naik", "laksarin.manager@sales.in", "Password123!", "sales_manager"),
        ]

        for name, email_addr, raw_pw, role in users_to_seed:
            user = User.query.filter_by(email=email_addr).first()
            if not user:
                print(f"Seeding user {email_addr} ({role})...")
                user = User(
                    name=name,
                    email=email_addr,
                    password_hash=generate_password_hash(raw_pw),
                    role=role,
                    is_active=True,
                )
                db.session.add(user)
        db.session.commit()

        # 2. Seed Manufacturing Companies with Tech Stacks (Requirement 6)
        c1 = Company.query.filter_by(name="Apex Precision Robotics").first()
        if not c1:
            print("Seeding Manufacturing sector companies with tech stacks...")
            c1 = Company(
                name="Apex Precision Robotics",
                industry="Industrial Automation & Robotics",
                size="1000-5000",
                annual_revenue=85000000.0,
                location="Detroit, MI, USA",
                employee_count=1450,
                website="https://apexprecisionrobotics.example.com",
                technology_stack="ROS2, Siemens S7 PLC, Fanuc CNC, IoT Edge",
                products_services="Automated Assembly Cells & Robotic Arms",
                funding="Parent Enterprise",
            )
            c2 = Company(
                name="Starlight Semiconductor Fab",
                industry="Semiconductor Manufacturing",
                size="5000+",
                annual_revenue=520000000.0,
                location="Hsinchu / Austin, TX, USA",
                employee_count=8500,
                website="https://starlightsemi.example.com",
                technology_stack="EUV Lithography, MES, Cleanroom Automation, SCADA",
                products_services="Advanced Silicon Wafers & Fab Machinery",
                funding="Public",
            )
            c3 = Company(
                name="Titan Industrial Heavy Machinery",
                industry="Heavy Machinery & Equipment",
                size="1000-5000",
                annual_revenue=240000000.0,
                location="Munich, Germany",
                employee_count=3800,
                website="https://titanheavymachinery.example.com",
                technology_stack="Hydraulic Systems, Siemens S7 PLC, SCADA, Heavy Forging",
                products_services="Heavy Hydraulic Presses & Foundry Systems",
                funding="Public Enterprise",
            )
            c4 = Company(
                name="Vanguard CNC Machining Systems",
                industry="CNC & Precision Tooling",
                size="500-1000",
                annual_revenue=45000000.0,
                location="Nagoya, Japan",
                employee_count=620,
                website="https://vanguardcnc.example.com",
                technology_stack="Fanuc CNC, High-Speed Spindles, CAD/CAM, AI Quality Control",
                products_services="5-Axis CNC Milling Centers & Lathes",
                funding="Private",
            )
            c5 = Company(
                name="Magna Auto Components",
                industry="Automotive Parts Manufacturing",
                size="1000-5000",
                annual_revenue=180000000.0,
                location="Stuttgart, Germany",
                employee_count=2900,
                website="https://magnaautocomponents.example.com",
                technology_stack="Automotive Stamping, Metal Joining, AI Vision Inspection",
                products_services="EV Powertrain & Chassis Assemblies",
                funding="Public",
            )
            db.session.add_all([c1, c2, c3, c4, c5])
            db.session.flush()

        # 3. Seed Contacts
        cnt1 = Contact.query.filter_by(email="v.mehta@apexprecision.example.com").first()
        if not cnt1 and c1:
            print("Seeding manufacturing contacts...")
            cnt1 = Contact(
                company_id=c1.id,
                name="Vikram Mehta",
                designation="VP of Manufacturing Operations",
                email="v.mehta@apexprecision.example.com",
                phone="+1-555-882-1920",
                is_decision_maker=True,
                decision_role="Head of Operations",
            )
            cnt2 = Contact(
                company_id=c2.id if c2 else None,
                name="Dr. Aris Thorne",
                designation="Director of Cleanroom Engineering",
                email="a.thorne@starlightsemi.example.com",
                phone="+1-555-401-9921",
                is_decision_maker=True,
                decision_role="Chief Fab Architect",
            )
            db.session.add_all([cnt1, cnt2])
            db.session.flush()

        # 4. Seed Real Manufacturing Dataset Leads (Requirement 2 & 6)
        if Lead.query.count() < 10:
            print("Seeding real manufacturing dataset leads...")
            if RAW_PIPELINE_PATH.exists():
                df = pd.read_csv(RAW_PIPELINE_PATH)
                sample_df = df.head(60)
                for idx, row in sample_df.iterrows():
                    company_name = str(row["account"]).strip()
                    contact_name = f"Agent {row['sales_agent']}"
                    email = f"contact.{idx}@{(company_name.lower().replace(' ', ''))}.example.com"
                    val = float(row["deal_value"]) if pd.notna(row["deal_value"]) else 125000.0
                    sector_val = str(row["sector"]).strip().replace("_", " ").title()

                    # Dynamic manufacturing tech stack based on sector
                    if "Semi" in sector_val:
                        t_stack = "EUV Lithography, MES, Cleanroom SCADA"
                    elif "Auto" in sector_val:
                        t_stack = "Automotive Stamping, ROS2, Vision Inspection"
                    elif "Tooling" in sector_val or "Cnc" in sector_val:
                        t_stack = "Fanuc CNC, High-Speed Spindles, CAD/CAM"
                    elif "Heavy" in sector_val:
                        t_stack = "Siemens S7 PLC, Heavy Hydraulics, SCADA"
                    else:
                        t_stack = "ROS2, Siemens S7 PLC, Fanuc CNC, IoT Edge"

                    lead_payload = {
                        "account": company_name,
                        "company": company_name,
                        "contact_name": contact_name,
                        "email": email,
                        "value": val,
                        "sector": sector_val,
                        "product": str(row["product"]).strip(),
                        "sales_agent": str(row["sales_agent"]).strip(),
                        "revenue": float(row["revenue"]) if pd.notna(row["revenue"]) else 85.0,
                        "employees": int(row["employees"]) if pd.notna(row["employees"]) else 1450,
                        "stage": "Won" if str(row["deal_stage"]).strip().lower() == "won" else "Qualified",
                    }

                    ml_input = build_ml_input(lead_payload)
                    prediction = predict_lead(ml_input)

                    lead = Lead(
                        company=company_name,
                        contact_name=contact_name,
                        email=email,
                        value=val,
                        sector=sector_val,
                        product=lead_payload["product"],
                        tech_stack=t_stack,
                        revenue=lead_payload["revenue"],
                        employees=lead_payload["employees"],
                        sales_agent=lead_payload["sales_agent"],
                        stage=lead_payload["stage"],
                        status="Open",
                        lead_score=prediction["lead_score"],
                        purchase_probability=prediction["purchase_probability"],
                    )
                    db.session.add(lead)
                db.session.commit()
                print(f"Seeded {len(sample_df)} real manufacturing leads with ML scores.")

        # 5. Generate AI Recommendations for All Leads
        print("Generating AI recommendations for all leads...")
        recs = generate_all_recommendations()
        print(f"Generated {len(recs)} active AI recommendations.")

        # 6. Seed CRM Connections
        if CRMConnection.query.count() == 0:
            print("Seeding CRM connection status...")
            crm1 = CRMConnection(
                provider="salesforce",
                account_name="Salesforce Enterprise Org (Manufacturing Cloud)",
                sync_status="Connected",
            )
            crm2 = CRMConnection(
                provider="hubspot",
                account_name="HubSpot Professional (Industrial Edition)",
                sync_status="Connected",
            )
            db.session.add(crm1)
            db.session.add(crm2)

        db.session.commit()
        print("Real-world dataset demo seed completed successfully!")


if __name__ == "__main__":
    seed()
