from werkzeug.security import generate_password_hash, check_password_hash
from app.repositories.user_repository import UserRepository
from app.repositories.owner_repository import OwnerRepository
from app.models.role import Role
from app.models.user import User
from app.models.owner import Owner
from app.States.context import UserContext  # <-- مهم
from app import db


class AccountService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.owner_repo = OwnerRepository()

    def get_role_by_name(self, role_name):
        return Role.query.filter_by(name=role_name).first()

    def user_register(self, fname, lname, username, email, password):
        hashed_password = generate_password_hash(password)

        # Get existing role from DB
        role = self.get_role_by_name("user")
        if not role:
            raise ValueError("Role 'user' not found in database.")

        user = User(
            fname=fname,
            lname=lname,
            username=username,
            email=email.strip().lower(),
            password=hashed_password,
            role=role  # <-- ربط مباشر
        )
        self.user_repo.create(user)
        return {"success": True, "account": user}

    def owner_register(self, fname, lname, username, email, password):
        hashed_password = generate_password_hash(password)

        role = self.get_role_by_name("owner")
        if not role:
            raise ValueError("Role 'owner' not found in database.")

        owner = Owner(
            fname=fname,
            lname=lname,
            username=username,
            email=email.strip().lower(),
            password=hashed_password,
            role=role
        )

        self.owner_repo.create(owner)
        return {"success": True, "account": owner}

    def login(self, email, password):
        email = email.strip().lower()

        user = self.user_repo.get_by_email(email)
        if user and check_password_hash(user.password, password):
            context = UserContext(user)
            return {
                "success": True,
                "account": user,
                "role": user.role.name if user.role else None,
                "state": context.state.__class__.__name__
            }

        owner = self.owner_repo.get_by_email(email)
        if owner and check_password_hash(owner.password, password):
            context = UserContext(owner)
            return {
                "success": True,
                "account": owner,
                "role": owner.role.name if owner.role else None,
                "state": context.state.__class__.__name__
            }

        return {"success": False, "message": "Invalid email or password"}
