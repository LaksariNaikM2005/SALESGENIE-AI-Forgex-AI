import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app import create_app
from backend.app.extensions import db, bcrypt
from backend.app.models import User, Company, Contact, Lead, LeadActivity, AIRecommendation, CRMConnection

def seed():
    app = create_app()
    with app.app_context():
        db.create_all()

        # Seed User
        if not User.query.filter_by(email="admin@salesgenie.ai").first():
            print("Seeding admin user...")
            hashed_pw = bcrypt.generate_password_hash("AdminPass123!").decode("utf-8")
            admin = User(
                name="System Administrator",
                email="admin@salesgenie.ai",
                password_hash=hashed_pw,
                role="admin",
                is_active=True
            )
            db.session.add(admin)

        # Seed Companies
        c1 = Company.query.filter_by(name="Acme Tech Solutions").first()
        if not c1:
            print("Seeding demo companies...")
            c1 = Company(
                name="Acme Tech Solutions",
                industry="Software & IT",
                size="100-500",
                annual_revenue=15000000.0,
                location="San Francisco, CA",
                employee_count=250,
                website="https://acmetech.example.com",
                technology_stack="Python, React, AWS, PostgreSQL",
                products_services="Cloud ERP & Analytics Platform",
                funding="Series B ($25M)",
            )
            c2 = Company(
                name="Global Logistics Corp",
                industry="Supply Chain & Freight",
                size="500-1000",
                annual_revenue=45000000.0,
                location="Chicago, IL",
                employee_count=750,
                website="https://globallogistics.example.com",
                technology_stack="Java, Oracle, Azure",
                products_services="Fleet Tracking & Supply Chain Software",
                funding="Public",
            )
            db.session.add(c1)
            db.session.add(c2)
            db.session.flush()

        # Seed Contacts
        cnt1 = Contact.query.filter_by(email="sarah.j@acmetech.example.com").first()
        if not cnt1 and c1:
            print("Seeding demo contacts...")
            cnt1 = Contact(
                company_id=c1.id,
                name="Sarah Jenkins",
                designation="Chief Technology Officer",
                email="sarah.j@acmetech.example.com",
                phone="+1-555-019-2834",
                is_decision_maker=True,
                decision_role="CTO",
            )
            db.session.add(cnt1)
            db.session.flush()

        # Seed Leads
        if Lead.query.count() == 0:
            print("Seeding demo leads...")
            l1 = Lead(
                company="Acme Tech Solutions",
                contact_name="Sarah Jenkins",
                email="sarah.j@acmetech.example.com",
                phone="+1-555-019-2834",
                stage="Qualified",
                status="Open",
                value=45000.0,
                lead_score=88.5,
                purchase_probability=0.82,
                response_time=1.5,
                sales_cycle=14.0,
                company_id=c1.id if c1 else None,
                contact_id=cnt1.id if cnt1 else None,
            )
            l2 = Lead(
                company="Global Logistics Corp",
                contact_name="David Miller",
                email="d.miller@globallogistics.example.com",
                phone="+1-555-014-9988",
                stage="Proposal",
                status="Open",
                value=85000.0,
                lead_score=92.0,
                purchase_probability=0.91,
                response_time=0.8,
                sales_cycle=10.0,
            )
            db.session.add(l1)
            db.session.add(l2)
            db.session.flush()

            # Add Lead Activity & Recommendation
            a1 = LeadActivity(
                lead_id=l1.id,
                activity_type="Website Visit",
                description="Visited pricing page and requested enterprise demo.",
            )
            rec1 = AIRecommendation(
                lead_id=l1.id,
                recommendation="High buying intent detected. Schedule technical demo with CTO Sarah Jenkins.",
                priority="High",
                reason="Company fits ideal profile and visited pricing page 3 times.",
            )
            db.session.add(a1)
            db.session.add(rec1)

        # Seed CRM Connections
        if CRMConnection.query.count() == 0:
            print("Seeding CRM connection status...")
            crm1 = CRMConnection(
                provider="salesforce",
                account_name="Salesforce Enterprise Org",
                sync_status="Connected",
            )
            crm2 = CRMConnection(
                provider="hubspot",
                account_name="HubSpot Professional",
                sync_status="Connected",
            )
            db.session.add(crm1)
            db.session.add(crm2)

        db.session.commit()
        print("Demo seed completed successfully!")

if __name__ == "__main__":
    seed()
