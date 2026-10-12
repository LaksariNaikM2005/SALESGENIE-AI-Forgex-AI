import getpass

from sqlalchemy import func, select

from app.core.security import hash_password
from app.database import Base, SessionLocal, engine
from app.models.user import User


def main():
    # For initial local development. In production, run Alembic migrations
    # before executing this script instead.
    Base.metadata.create_all(bind=engine)

    name = input("Admin name: ").strip()
    email = input("Admin email: ").strip().lower()
    password = getpass.getpass("Admin password (12+ characters): ")
    confirm = getpass.getpass("Confirm password: ")

    if len(name) < 2 or len(password) < 12:
        raise SystemExit("Name or password does not meet requirements.")

    if password != confirm:
        raise SystemExit("Passwords do not match.")

    with SessionLocal.begin() as db:
        existing_admin = db.scalar(
            select(func.count())
            .select_from(User)
            .where(User.role == "admin")
        )

        if existing_admin:
            raise SystemExit(
                "An Admin already exists. Use the Admin dashboard."
            )

        existing_email = db.scalar(
            select(User.id).where(User.email == email)
        )

        if existing_email:
            raise SystemExit("That email is already registered.")

        db.add(
            User(
                name=name,
                email=email,
                password_hash=hash_password(password),
                role="admin",
                is_active=True,
            )
        )

    print("First Admin created successfully.")


if __name__ == "__main__":
    main()