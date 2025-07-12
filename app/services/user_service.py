""""
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.role import Role
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.controllers.account import Account

class UserService(Account):
    def __init__(self):
        self.repo = UserRepository()

    def register(self, first_name, last_name, user_name, email, password):
        existing_user = self.repo.get_by_email(email)
        if existing_user:
            return {"success": False, "message": "Email already registered"}

        hashed_password = generate_password_hash(password)

        role = self.get_role()
        if not role:
            return {"success": False, "message": "User role not found in DB"}

        new_user = User(
            fname=first_name,
            lname=last_name,
            username=user_name,
            email=email,
            password=hashed_password,
            role_id=role.id
        )

        db.session.add(new_user)
        db.session.commit()

        return {"success": True, "user": new_user.to_dict()}

    def login(self, email, password):
        user = self.repo.get_by_email(email)
        if user and check_password_hash(user.password, password):
            return {"success": True, "user": user}
        return {"success": False, "message": "Invalid credentials"}

    def get_role(self):
        return Role.query.filter_by(name="user").first()
"""