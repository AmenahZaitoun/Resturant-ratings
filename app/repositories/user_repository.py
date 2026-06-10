from app.repositories.base_repository import Repository
from app.models.user import User
from app.models.role import Role
from app import db

class UserRepository(Repository):
    def create(self, user):
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user):
        db.session.commit()
        return user

    def get(self, user_id):
        return db.session.get(User, user_id)

    def get_by_username(self, username):
        return db.session.query(User).filter_by(username=username).first()

    def get_role(self, email):
        user = self.get_by_email(email)
        if user:
            return Role.query.get(user.role_id)  
        return None

    def get_all(self):
        return User.query.all()
    
    def get_by_email(self, email):
        return db.session.query(User).filter_by(email=email.strip().lower()).first()

    def delete(self, user_id):
        user = self.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

        
