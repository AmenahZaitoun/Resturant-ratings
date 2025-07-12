from app.repositories.base_repository import Repository
from app.models.owner import Owner
from app.models.role import Role
from app import db

class OwnerRepository(Repository):
    def create(self, owner):
        db.session.add(owner)
        db.session.commit()
        return owner
    
    def update(self, Owner):
        db.session.commit()
        return Owner
    
    def get(self, username):
        return Owner.query.get(username)
    def get_role(self, email):
        owner = self.get_by_email(email)
        if owner:
            return Role.query.get(owner.role_id)  
        return None
    def get_by_email(self, email):
        return db.session.query(Owner).filter_by(email=email.strip().lower()).first()
   
    def get_all(self):
        return Owner.query.all()
    
    def delete(self, username):
        user = self.get(username)
        if user:
            db.session.delete(user)
            db.session.commit()

