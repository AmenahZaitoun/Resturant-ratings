from app import db

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    facilities = db.relationship("Facilities", backref="owner", lazy=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role')
    def __repr__(self):
        return f"<Owner {self.username} - {self.email}>"
