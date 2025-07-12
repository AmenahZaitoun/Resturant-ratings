"""
from app.repositories.owner_repository import OwnerRepository
from app.models.owner import Owner
from app.models.role import Role
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.controllers.account import Account

class OwnerService(Account):
    def __init__(self):
        self.repo = OwnerRepository()

    def register(self, fname, lname, username, email, password):
        existing_owner = self.repo.get_by_email(email)
        if existing_owner:
            return {"success": False, "message": "Email already registered"}

        hashed_password = generate_password_hash(password)

        role = self.get_role()
        if not role:
            return {"success": False, "message": "Owner role not found in DB"}

        new_owner = Owner(
            fname=fname,
            lname=lname,
            username=username,
            email=email,
            password=hashed_password,
            role_id=role.id
        )

        db.session.add(new_owner)
        db.session.commit()

        return {"success": True, "owner": new_owner.to_dict()}

    def login(self, email, password):
        owner = self.repo.get_by_email(email)
        if owner and check_password_hash(owner.password, password):
            return {"success": True, "owner": owner}
        return {"success": False, "message": "Invalid credentials"}

    def get_role(self):
        return Role.query.filter_by(name="owner").first()
"""