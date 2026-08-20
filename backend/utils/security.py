from flask_bcrypt import Bcrypt

# Initialize Bcrypt without the app object (it will be bound in app.py)
bcrypt = Bcrypt()

def hash_password(password):
    """Generates a secure hash for a new user's password."""
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(password_hash, password):
    """Verifies a password during the login process."""
    return bcrypt.check_password_hash(password_hash, password)