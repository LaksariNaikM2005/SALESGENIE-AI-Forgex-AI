import getpass

from werkzeug.security import generate_password_hash

from backend.app import create_app
from backend.app.extensions import db
from backend.app.models import User


def main():
    email = input("Admin email: ").strip().lower()
    name = input("Admin name: ").strip()
    password = getpass.getpass("Admin password: ")
    confirm = getpass.getpass("Confirm password: ")

    if not email or not name:
        raise SystemExit("Name and email are required.")

    if len(password) < 12:
        raise SystemExit("Use a password with at least 12 characters.")

    if password != confirm:
        raise SystemExit("Passwords do not match.")

    app = create_app()

    with app.app_context():
        existing = User.query.filter_by(email=email).first()

        if existing:
            raise SystemExit(
                "This email already exists. No changes were made."
            )

        admin = User(
                    name=name,
                    email=email,
                    password_hash=generate_password_hash(password),
                    role="admin",
                    is_active=True,
                )

        db.session.add(admin)
        db.session.commit()

        print("Admin account created successfully.")


if __name__ == "__main__":
    main()