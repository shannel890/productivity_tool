from flask import Flask
from app import create_app
from app.models import db, Role, User
from flask_security.utils import hash_password
import datetime

def init_db():
    app = create_app()
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Create roles if they don't exist
        roles = {
            'admin': 'Administrator',
            'user': 'Regular User'
        }
        
        for role_name, role_desc in roles.items():
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                role = Role(name=role_name, description=role_desc)
                db.session.add(role)
                print(f"Created {role_name} role")
        
        # Create admin user if it doesn't exist
        admin_email = 'admin@example.com'
        admin_user = User.query.filter_by(email=admin_email).first()
        admin_role = Role.query.filter_by(name='admin').first()
        
        if not admin_user and admin_role:
            admin_user = User(
                email=admin_email,
                password=hash_password('admin123'),  # Change this in production!
                active=True,
                confirmed_at=datetime.datetime.utcnow()
            )
            admin_user.roles.append(admin_role)
            db.session.add(admin_user)
            print(f"Created admin user: {admin_email}")
        
        try:
            db.session.commit()
            print("Database initialized successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing database: {str(e)}")

if __name__ == '__main__':
    init_db()
